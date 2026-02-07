"""
Agentic chatbot powered by LangGraph.

Graph topology (nodes are agents, edges show data flow):

        ┌──────────┐
  query │          │
 ──────►  ROUTER   │
        │          │
        └────┬─────┘
             │ topic == "off_topic"   →  OFF_TOPIC_NODE  →  end
             │ topic != "off_topic"
             ▼
        ┌──────────┐
        │RETRIEVER │   (metadata-filtered FAISS lookup)
        └────┬─────┘
             │
             ▼
        ┌───────────┐
        │ VALIDATOR │
        └────┬──────┘
             │ INSUFFICIENT  →  INSUFFICIENT_NODE  →  end
             │ SUFFICIENT
             ▼
        ┌───────────┐
        │ RESPONDER │  →  end
        └───────────┘

Session memory (last N messages) is threaded through every node via the
GraphState TypedDict so the Responder can maintain conversational continuity.
"""

from typing import List, Dict, TypedDict
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from src.rag_engine import RAGEngine
from config import settings
from config.prompts import (
    TOPIC_MAP,
    ROUTER_PROMPT,
    VALIDATOR_PROMPT,
    RESPONDER_PROMPT,
    OFF_TOPIC_PROMPT,
    INSUFFICIENT_CONTEXT_PROMPT,
    GREETING_PROMPT,
    FAREWELL_PROMPT,
)


# ---------------------------------------------------------------------------
# State shared across every node in the graph
# ---------------------------------------------------------------------------
class GraphState(TypedDict):
    query: str                      # original user question
    topic: str                      # topic assigned by Router (or "off_topic")
    context: str                    # chunks returned by Retriever
    validation: str                 # "SUFFICIENT" | "INSUFFICIENT"
    response: str                   # final answer
    chat_history: str               # formatted history string


# ---------------------------------------------------------------------------
# LLM factory (shared by all agents)
# ---------------------------------------------------------------------------
def _build_llm():
    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            openai_api_key=settings.OPENAI_API_KEY,
        )
    if settings.LLM_PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_output_tokens=settings.MAX_TOKENS,
            google_api_key=settings.GOOGLE_API_KEY,
        )
    if settings.LLM_PROVIDER == "groq":
        return ChatGroq(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            api_key=settings.GROQ_API_KEY,
            reasoning_format= "hidden",
        )
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")


# ---------------------------------------------------------------------------
# Node implementations
# ---------------------------------------------------------------------------
def router_node(state: GraphState, llm) -> GraphState:
    """Classify the query into one of the canonical topics or 'off_topic'."""
    prompt = ROUTER_PROMPT.format(query=state["query"])
    raw = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    print(raw)
    
    # Normalise: accept any capitalisation, strip punctuation
    candidate = raw.strip(".\n \"'").strip()
    # Match against known topics (case-insensitive)
    matched = "off_topic"
    for key in TOPIC_MAP:
        if key.lower() == candidate.lower():
            matched = key
            break

    return {**state, "topic": matched}


def retriever_node(state: GraphState, rag: RAGEngine) -> GraphState:
    """Fetch chunks filtered by the topic the Router assigned."""
    topic = state["topic"]
    # Pass topic to the metadata-filtered retriever
    context = rag.retrieve_formatted(state["query"], topic=topic)
    return {**state, "context": context}


def validator_node(state: GraphState, llm) -> GraphState:
    """Decide whether the retrieved context is sufficient to answer."""
    prompt = VALIDATOR_PROMPT.format(
        query=state["query"], context=state["context"]
    )
    raw = llm.invoke([HumanMessage(content=prompt)]).content.strip().upper()
    # verdict = "SUFFICIENT" if "SUFFICIENT" in raw else "INSUFFICIENT"
    verdict = "PASS" if "PASS" in raw else "FAIL"
    return {**state, "validation": verdict}


def responder_node(state: GraphState, llm) -> GraphState:
    """Generate the final human-like answer from validated context."""
    prompt = RESPONDER_PROMPT.format(
        context=state["context"],
        chat_history=state["chat_history"],
        question=state["query"],
    )
    answer = llm.invoke(
        [SystemMessage(content="You are a professional AI assistant."),
         HumanMessage(content=prompt)]
    ).content.strip()
    return {**state, "response": answer}


def off_topic_node(state: GraphState, llm) -> GraphState:
    """Politely redirect off-topic queries."""
    prompt = OFF_TOPIC_PROMPT.format(query=state["query"])
    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {**state, "response": answer}


def insufficient_node(state: GraphState, llm) -> GraphState:
    """Honest fallback when chunks don't cover the question."""
    prompt = INSUFFICIENT_CONTEXT_PROMPT.format(query=state["query"])
    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {**state, "response": answer}


# ---------------------------------------------------------------------------
# Conditional edge helpers
# ---------------------------------------------------------------------------
def route_after_router(state: GraphState) -> str:
    return "off_topic" if state["topic"] == "off_topic" else "retriever"


def route_after_validator(state: GraphState) -> str:
    return "responder" if state["validation"] == "PASS" else "insufficient"


# ---------------------------------------------------------------------------
# Graph builder  (called once; the compiled graph is reused)
# ---------------------------------------------------------------------------
def _build_graph(llm, rag: RAGEngine) -> "CompiledGraph":
    """Wire up nodes + edges and compile the LangGraph."""
    builder = StateGraph(GraphState)

    # ── Nodes (wrap closures to inject llm / rag) ──
    builder.add_node("router",       lambda s: router_node(s, llm))
    builder.add_node("retriever",    lambda s: retriever_node(s, rag))
    builder.add_node("validator",    lambda s: validator_node(s, llm))
    builder.add_node("responder",    lambda s: responder_node(s, llm))
    builder.add_node("off_topic",    lambda s: off_topic_node(s, llm))
    builder.add_node("insufficient", lambda s: insufficient_node(s, llm))

    # ── Edges ──
    builder.set_entry_point("router")

    # Router → retriever OR off_topic
    builder.add_conditional_edges("router", route_after_router)

    # Retriever always flows to validator
    builder.add_edge("retriever", "validator")

    # Validator → responder OR insufficient
    # builder.add_conditional_edges("validator", route_after_validator)
    builder.add_conditional_edges(
        "validator",
        route_after_validator,
        path_map= {
            "responder"     : "responder",
            "insufficient"  : "insufficient",
        }
    )

    # Terminal nodes
    builder.add_edge("responder",    END)
    builder.add_edge("off_topic",    END)
    builder.add_edge("insufficient", END)

    return builder.compile()


# ---------------------------------------------------------------------------
# Public façade: ProfileChatbot
# ---------------------------------------------------------------------------
class ProfileChatbot:
    """
    Thin wrapper around the compiled LangGraph.

    Manages session memory and exposes greeting / farewell helpers.
    """

    def __init__(self, rag: RAGEngine):
        self.llm = _build_llm()
        self.graph = _build_graph(self.llm, rag)
        self.history: List[Dict[str, str]] = []   # [{role, content}, ...]

    # ------------------------------------------------------------------
    # Core chat entry-point
    # ------------------------------------------------------------------
    def chat(self, query: str) -> str:
        # Detect greetings / farewells before hitting the graph
        lower = query.lower().strip()
        if lower in {"hello", "hi", "hey", "greetings", "good morning", "good afternoon"}:
            reply = self.get_greeting()
            self._push("user", query)
            self._push("assistant", reply)
            return reply

        if any(w in lower for w in ("bye", "goodbye", "thank you", "thanks", "see you", "stop", "exit")):
            reply = self.get_farewell()
            self._push("user", query)
            self._push("assistant", reply)
            return reply

        # Feed through the LangGraph pipeline
        initial_state: GraphState = {
            "query":        query,
            "topic":        "",
            "context":      "",
            "validation":   "",
            "response":     "",
            "chat_history": self._format_history(),
        }

        try:
            final_state = self.graph.invoke(initial_state)
            reply = final_state["response"]
        except Exception:
            reply = (
                "I hit a small snag processing that — could you try rephrasing? "
                "I'm happy to help with anything about the profile."
            )

        self._push("user", query)
        self._push("assistant", reply)
        return reply

    # ------------------------------------------------------------------
    # Greeting / farewell (LLM-generated, with static fallbacks)
    # ------------------------------------------------------------------
    def get_greeting(self) -> str:
        try:
            return self.llm.invoke(
                [HumanMessage(content=GREETING_PROMPT)]
            ).content.strip()
        except Exception:
            # return (
            #     f"Hello! I'm an AI assistant for {settings.DEVELOPER_NAME}, "
            #     "a Senior AI/ML Specialist. Ask me about experience, projects, "
            #     "skills, or background — I'm happy to help!"
            # )
            return (
                f"I’m the AI voice 🤖 of {settings.DEVELOPER_NAME}, "
                "a Senior AI/ML Specialist. Let's discuss about my experience, projects, "
                "skills, or background — I'm happy to answer!"
            )

    def get_farewell(self) -> str:
        try:
            return self.llm.invoke(
                [HumanMessage(content=FAREWELL_PROMPT)]
            ).content.strip()
        except Exception:
            return (
                "Thank you for your interest!\n\n"
                f"📧 Email: {settings.PROFILE_INFO['email']}\n"
                f"💼 LinkedIn: {settings.PROFILE_INFO['linkedin']}\n\n"
                "Looking forward to connecting!"
            )

    # ------------------------------------------------------------------
    # History management
    # ------------------------------------------------------------------
    def _push(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        # Keep window bounded
        if len(self.history) > settings.MAX_CONVERSATION_HISTORY:
            self.history = self.history[-settings.MAX_CONVERSATION_HISTORY:]

    def _format_history(self) -> str:
        if not self.history:
            return "No previous conversation."
        lines = []
        for msg in self.history[-6:]:          # last 3 exchanges
            label = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{label}: {msg['content']}")
        return "\n".join(lines)

    def clear_history(self) -> None:
        self.history.clear()

    def get_history(self) -> List[Dict[str, str]]:
        return list(self.history)