"""
Configuration settings for the AI Digital Profile.

Every tuneable value lives here or in .env so that nothing is scattered
across source files.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# LLM API Keys
# ---------------------------------------------------------------------------
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY  = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")

# ---------------------------------------------------------------------------
# QDRANT Cloud hosting API Keys
# ---------------------------------------------------------------------------
VECTORDB_URL = os.getenv('VECTORDB_URL')
VECTORDB_API_KEY = os.getenv('VECTORDB_API_KEY')
VECTORDB_COLLECTION_NAME = os.getenv('VECTORDB_COLLECTION_NAME')

# ---------------------------------------------------------------------------
# LLM / Embedding selection
# ---------------------------------------------------------------------------
LLM_PROVIDER      = os.getenv("LLM_PROVIDER", "openai")   # "openai" | "google"
MODEL_NAME        = os.getenv("MODEL_NAME", "gpt-4o")
TEMPERATURE       = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS        = int(os.getenv("MAX_TOKENS", "1000"))
# EMBEDDING_MODEL   = "text-embedding-3-small"               # OpenAI default
# EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1"  # nomic-ai default
EMBEDDING_MODEL   = os.getenv("EMBEDDING_MODEL")


# ---------------------------------------------------------------------------
# Vector Store  (pre-built; never recreated at runtime)
# ---------------------------------------------------------------------------
RESUME_FILE = os.getenv("RESUME_FILE", "media/About_me.docx")
VECTOR_STORE_LOCATION = os.getenv("VECTOR_STORE_LOCATION", "local")

# For Local Hosting
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")

# for Remote Hosting
VECTOR_STORE_HOST = os.getenv("VECTOR_STORE_HOST")

# How many chunks the retriever returns when filtering by topic
TOP_K_RESULTS     = int(os.getenv("TOP_K_RESULTS", "4"))

# ---------------------------------------------------------------------------
# Embedding Parameters
# ---------------------------------------------------------------------------
CHUNK_WARNING_THRESHOLD = int(os.getenv("CHUNK_THRESHOLD", "500"))
# How many chunks overlap between two chunks
CHUNK_OVERLAP_SIZE     = int(os.getenv("CHUNK_OVERLAP_SIZE", "50"))

# ---------------------------------------------------------------------------
# Profile – update with your real links before deploying
# ---------------------------------------------------------------------------
PROFILE_INFO = {
    "name"      :    "Vivek Joseph Carvalho",
    "title"     :    "Senior AI/ML Specialist | Agentic AI Developer | Data Scientist | Data Specialist",
    "location"  :    "Mumbai, India",
    "email"     :    "vivek_carvalho@yahoo.co.in",
    "linkedin"  :    "https://www.linkedin.com/in/vivekcarvalho/",
    "github"    :    "https://github.com/vivekcarvalho",
    # "portfolio":   "https://vivekcarvalho.com",
    "whatsapp"  :    os.getenv("WHATSAPP_NO"),
    "mobile"    :    os.getenv("MOBILE_NO"),
}
DEVELOPER_NAME = PROFILE_INFO["name"]
PROFILE_PICTURE_PATH = "media/profile_pic.jpeg"

# ---------------------------------------------------------------------------
# Chatbot UI
# ---------------------------------------------------------------------------
CHATBOT_AVATAR          = "assets/profile_photo.jpg"
USER_AVATAR             = "👤"
MAX_CONVERSATION_HISTORY = 20   # messages kept for context window

# ---------------------------------------------------------------------------
# Validation Agent Configuration
# ---------------------------------------------------------------------------
ALLOWED_TOPICS = [
    "experience", "education", "skills", "projects", "certifications",
    "achievements", "background", "career", "expertise", "qualifications",
    "portfolio", "contact", "resume", "cv", "profile", "about", "weakness"
]

# ---------------------------------------------------------------------------
# Blocked Topics (for safety and relevance)
# ---------------------------------------------------------------------------
BLOCKED_TOPICS = [
    "political", "religion", "personal opinions", "controversial",
    "medical advice", "legal advice", "financial advice"
]