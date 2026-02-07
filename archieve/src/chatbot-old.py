"""
Chatbot module with RAG-enabled conversational AI
"""
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from src.rag_engine import RAGEngine
from config import settings, prompts


class ProfileChatbot:
    """AI Chatbot with RAG for profile queries"""
    
    def __init__(self, rag_engine: RAGEngine):
        """
        Initialize chatbot
        
        Args:
            rag_engine: RAG engine instance
        """
        self.rag_engine = rag_engine
        self.llm = self._initialize_llm()
        self.conversation_history: List[Dict[str, str]] = []
        
    def _initialize_llm(self):
        """Initialize LLM based on configuration"""
        if settings.LLM_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found")
            return ChatOpenAI(
                model=settings.MODEL_NAME,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                openai_api_key=settings.OPENAI_API_KEY
            )
        elif settings.LLM_PROVIDER == "google":
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not found")
            return ChatGoogleGenerativeAI(
                model=settings.MODEL_NAME,
                temperature=settings.TEMPERATURE,
                max_output_tokens=settings.MAX_TOKENS,
                google_api_key=settings.GOOGLE_API_KEY
            )
        else:
            raise ValueError(f"Unsupported provider: {settings.LLM_PROVIDER}")
    
    def _check_query_relevance(self, query: str) -> bool:
        """
        Check if query is relevant to profile discussion
        
        Args:
            query: User query
            
        Returns:
            True if relevant, False otherwise
        """
        # Simple keyword-based check
        query_lower = query.lower()
        
        # Check for blocked topics
        for blocked in settings.BLOCKED_TOPICS:
            if blocked in query_lower:
                return False
        
        # Check for allowed topics
        for allowed in settings.ALLOWED_TOPICS:
            if allowed in query_lower:
                return True
        
        # Use LLM for complex cases
        try:
            relevance_prompt = prompts.QUERY_RELEVANCE_PROMPT.format(query=query)
            messages = [HumanMessage(content=relevance_prompt)]
            response = self.llm.invoke(messages)
            
            return "RELEVANT" in response.content.upper()
        except:
            # Default to relevant if LLM check fails
            return True
    
    def _format_chat_history(self) -> str:
        """Format conversation history for context"""
        if not self.conversation_history:
            return "No previous conversation."
        
        formatted = []
        for msg in self.conversation_history[-5:]:  # Last 5 exchanges
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def get_greeting(self) -> str:
        """Generate a greeting message"""
        try:
            messages = [HumanMessage(content=prompts.GREETING_PROMPT)]
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            # Fallback greeting
            return (
                f"Hello! I'm an AI assistant representing {settings.DEVELOPER_NAME}, "
                "a Senior AI/ML Specialist. Feel free to ask about experience, "
                "skills, projects, or background. How can I help you today?"
            )
    
    def get_farewell(self) -> str:
        """Generate a farewell message"""
        try:
            messages = [HumanMessage(content=prompts.FAREWELL_PROMPT)]
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            # Fallback farewell
            return (
                "Thank you for your interest! Feel free to reach out:\n\n"
                f"📧 Email: {settings.PROFILE_INFO['email']}\n"
                f"💼 LinkedIn: {settings.PROFILE_INFO['linkedin']}\n\n"
                "Looking forward to connecting!"
            )
    
    def chat(self, query: str) -> str:
        """
        Process a chat query
        
        Args:
            query: User question
            
        Returns:
            Chatbot response
        """
        # Check for greetings
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]
        if query.lower().strip() in greetings:
            response = self.get_greeting()
            self._add_to_history("user", query)
            self._add_to_history("assistant", response)
            return response
        
        # Check for farewells
        farewells = ["bye", "goodbye", "thank you", "thanks", "see you"]
        if any(word in query.lower() for word in farewells):
            response = self.get_farewell()
            self._add_to_history("user", query)
            self._add_to_history("assistant", response)
            return response
        
        # Check query relevance
        if not self._check_query_relevance(query):
            response = self._generate_off_topic_response(query)
            self._add_to_history("user", query)
            self._add_to_history("assistant", response)
            return response
        
        # Retrieve context from vector store
        context = self.rag_engine.get_formatted_context(query)
        
        # Format conversation history
        chat_history = self._format_chat_history()
        
        # Create conversation prompt
        conversation_prompt = prompts.CONVERSATION_PROMPT.format(
            context=context,
            chat_history=chat_history,
            question=query
        )
        
        # Generate response
        try:
            messages = [
                SystemMessage(content=prompts.SYSTEM_PROMPT),
                HumanMessage(content=conversation_prompt)
            ]
            
            response = self.llm.invoke(messages)
            answer = response.content.strip()
            
            # Add to history
            self._add_to_history("user", query)
            self._add_to_history("assistant", answer)
            
            return answer
            
        except Exception as e:
            error_msg = (
                "I apologize, but I encountered an error processing your question. "
                "Please try rephrasing or ask something else about the profile."
            )
            return error_msg
    
    def _generate_off_topic_response(self, query: str) -> str:
        """Generate response for off-topic queries"""
        try:
            off_topic_prompt = prompts.OFF_TOPIC_PROMPT.format(query=query)
            messages = [HumanMessage(content=off_topic_prompt)]
            response = self.llm.invoke(messages)
            return response.content.strip()
        except:
            return (
                "I appreciate your question, but I focus on professional topics "
                f"related to {settings.DEVELOPER_NAME}'s career, skills, and experience. "
                "Feel free to ask about AI/ML projects, technical expertise, "
                "work experience, or educational background!"
            )
    
    def _add_to_history(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Limit history size
        if len(self.conversation_history) > settings.MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-settings.MAX_CONVERSATION_HISTORY:]
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()