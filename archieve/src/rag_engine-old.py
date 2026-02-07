"""
RAG Engine - Handles vector database operations and retrieval
"""
import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from config import settings


class RAGEngine:
    """Retrieval-Augmented Generation engine for profile queries"""
    
    def __init__(self, vector_store_path: str = None):
        """
        Initialize RAG engine
        
        Args:
            vector_store_path: Path to FAISS vector store
        """
        self.vector_store_path = vector_store_path or settings.VECTOR_STORE_PATH
        self.embeddings = self._initialize_embeddings()
        self.vector_store = None
        self.retriever = None
        
    def _initialize_embeddings(self):
        """Initialize embedding model based on configuration"""
        if settings.LLM_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY
            )
        elif settings.LLM_PROVIDER == "google":
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not found in environment")
            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GOOGLE_API_KEY
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
    
    def create_vector_store(self, text: str, save: bool = True) -> None:
        """
        Create vector store from text
        
        Args:
            text: Profile text to index
            save: Whether to save to disk
        """
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        print(f"Created {len(documents)} chunks from profile data")
        
        # Create vector store
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        
        # Save to disk
        if save:
            os.makedirs(self.vector_store_path, exist_ok=True)
            self.vector_store.save_local(self.vector_store_path)
            print(f"Vector store saved to {self.vector_store_path}")
        
        # Initialize retriever
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": settings.TOP_K_RESULTS}
        )
    
    def load_vector_store(self) -> None:
        """Load vector store from disk"""
        if not os.path.exists(self.vector_store_path):
            raise FileNotFoundError(
                f"Vector store not found at {self.vector_store_path}. "
                "Please run setup_vectordb.py first."
            )
        
        try:
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            self.retriever = self.vector_store.as_retriever(
                search_kwargs={"k": settings.TOP_K_RESULTS}
            )
            print(f"Vector store loaded successfully from {self.vector_store_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load vector store: {str(e)}")
    
    def retrieve_context(self, query: str) -> List[str]:
        """
        Retrieve relevant context for a query
        
        Args:
            query: User query
            
        Returns:
            List of relevant text chunks
        """
        if not self.retriever:
            raise RuntimeError("Retriever not initialized. Load vector store first.")
        
        # Retrieve relevant documents
        docs = self.retriever.get_relevant_documents(query)
        
        # Extract text content
        contexts = [doc.page_content for doc in docs]
        
        return contexts
    
    def get_formatted_context(self, query: str) -> str:
        """
        Get formatted context string for LLM
        
        Args:
            query: User query
            
        Returns:
            Formatted context string
        """
        contexts = self.retrieve_context(query)
        
        if not contexts:
            return "No relevant information found."
        
        # Format context with separators
        formatted = "\n\n---\n\n".join(contexts)
        return formatted
    
    def similarity_search(self, query: str, k: int = 5) -> List[tuple]:
        """
        Perform similarity search with scores
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results


# Singleton instance
_rag_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    """Get or create RAG engine singleton"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
        _rag_engine.load_vector_store()
    return _rag_engine