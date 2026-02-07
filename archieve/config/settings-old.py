"""
Configuration settings for the AI Profile Website
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "google"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))

# Embedding Configuration
# EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI default
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1"  # nomic-ai default
EMBEDDING_DIMENSION = 1536

# Example using LangChain with HuggingFace
# from langchain_huggingface import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1")
# text = "This is a sample document."
# query_result = embeddings.embed_query(text)


# Vector Store Configuration
VECTOR_STORE_PATH = "data/vector_store"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K_RESULTS = 4  # Number of chunks to retrieve

# Application Settings
APP_TITLE = os.getenv("APP_TITLE", "AI-Powered Digital Profile")
DEVELOPER_NAME = os.getenv("DEVELOPER_NAME", "Vivek Joseph Carvalho")

# Profile Information (Update these with your details)
PROFILE_INFO = {
    "name": "Vivek Joseph Carvalho",
    "title": "Senior AI/ML Specialist | Data Scientist | Agentic AI Developer",
    "location": "Mumbai, India",
    "email": "vivek_carvalho@yahoo.co.in",
    "linkedin": "https://www.linkedin.com/in/vivekcarvalho/",
    "github": "https://github.com/vivekcarvalho",
    "phone": "+91-XXXXXXXXXX"
}

# Chatbot Configuration
CHATBOT_NAME = "AI Assistant"
CHATBOT_AVATAR = "media/profile_pic.jpeg"
USER_AVATAR = "👤"

# Session Configuration
SESSION_TIMEOUT_MINUTES = 30
MAX_CONVERSATION_HISTORY = 20

# Validation Configuration
ALLOWED_TOPICS = [
    "experience", "education", "skills", "projects", "certifications",
    "achievements", "background", "career", "expertise", "qualifications",
    "portfolio", "contact", "resume", "cv", "profile", "about"
]

# Blocked Topics (for safety and relevance)
BLOCKED_TOPICS = [
    "political", "religion", "personal opinions", "controversial",
    "medical advice", "legal advice", "financial advice"
]