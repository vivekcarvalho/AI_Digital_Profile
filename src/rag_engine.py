"""
RAG Engine – loads the pre-built FAISS vector store and exposes
metadata-filtered retrieval.

Design constraints:
  • The vector store is NEVER created here.  It is assumed to already exist
    at VECTOR_STORE_PATH with each chunk carrying a metadata["topic"] field
    whose value matches one of the keys in prompts.TOPIC_MAP.
  • The public method retrieve(query, topic) accepts an optional topic string.
    When supplied it passes a metadata equality filter to FAISS so that only
    chunks from that topic are considered.
  • A module-level singleton (get_rag_engine()) keeps the FAISS index in memory
    across Streamlit reruns without reloading from disk every time.
"""

import os
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from data.build_vector_store import NomicEmbedding

from config import settings


class RAGEngine:
    """Load and query the pre-built FAISS vector store."""

    def __init__(self, vector_store_path: str | None = None):
        self.vector_store_path = vector_store_path or settings.VECTOR_STORE_PATH
        self.embeddings = self._init_embeddings()
        self.vector_store: Optional[FAISS] = None

    # ------------------------------------------------------------------
    # Embedding model selection
    # ------------------------------------------------------------------
    def _init_embeddings(self):
        if settings.LLM_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set.")
            return OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY,
            )
        if settings.LLM_PROVIDER == "google":
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is not set.")
            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GOOGLE_API_KEY,
            )
        if settings.EMBEDDING_MODEL:
            return NomicEmbedding.create_embedding(
                model_name= settings.EMBEDDING_MODEL,
                model_kwargs= {'trust_remote_code': True,},
                encode_kwargs={"normalize_embeddings": False,},
                show_progress = False
            )
        raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")

    # ------------------------------------------------------------------
    # Load from disk (once)
    # ------------------------------------------------------------------
    def load(self) -> None:
        """Load the pre-built FAISS store from disk."""
        if not os.path.exists(self.vector_store_path):
            raise FileNotFoundError(
                f"Vector store not found at '{self.vector_store_path}'.\n"
                "Build it once with:  python scripts/setup_vectordb.py"
            )
        self.vector_store = FAISS.load_local(
            self.vector_store_path,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    # ------------------------------------------------------------------
    # Core retrieval – the only public query method
    # ------------------------------------------------------------------
    def retrieve(self, query: str, topic: str | None = None) -> List[str]:
        """
        Return the text of the top-k most-relevant chunks.

        Parameters
        ----------
        query : str
            The semantic query fed to the embedding model.
        topic : str | None
            When provided, only chunks whose metadata["topic"] == topic are
            considered.  This is the key mechanism that makes retrieval
            context-aware and avoids mixing unrelated profile sections.

        Returns
        -------
        List[str]
            Chunk texts ordered by similarity (most relevant first).
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not loaded. Call .load() first.")

        # Build the search filter when a topic is given
        search_filter = (
            {"title": topic} if topic else None
        )

        # as_retriever with dynamic search_kwargs lets us pass the filter
        retriever = self.vector_store.as_retriever(
            search_kwargs={
                "k": settings.TOP_K_RESULTS,
                "fetch_k": settings.FETCH_RESULTS,
                **({"filter": search_filter} if search_filter else {}),
            }
        )

        docs = retriever.invoke(query)
        return [doc.page_content for doc in docs]

    # ------------------------------------------------------------------
    # Convenience: formatted context string for the Responder prompt
    # ------------------------------------------------------------------
    def retrieve_formatted(self, query: str, topic: str | None = None) -> str:
        chunks = self.retrieve(query, topic)
        return "\n\n---\n\n".join(chunks) if chunks else ""


# ---------------------------------------------------------------------------
# Module-level singleton so Streamlit doesn't reload from disk on every rerun
# ---------------------------------------------------------------------------
_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    global _engine
    if _engine is None:
        _engine = RAGEngine()
        _engine.load()
    return _engine