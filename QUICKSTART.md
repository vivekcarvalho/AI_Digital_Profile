# AI-Powered Digital Profile Website

A recruiter-facing digital profile with a **LangGraph multi-agent chatbot** backed by topic-filtered RAG retrieval. The Home page presents a polished, resume-style summary; the AI Chatbot page lets visitors ask natural-language questions and get context-aware, hallucination-resistant answers.

---

## ✨ What makes this different

| Feature | How it works |
|---|---|
| **LangGraph agentic pipeline** | Every query passes through Router → Retriever → Validator → Responder agents with conditional edges. Off-topic and insufficient-context queries are handled gracefully by dedicated fallback nodes. |
| **Metadata-filtered RAG** | The pre-built FAISS vector store tags every chunk with a `title` field (Introduction, Education, Job Summary, Project Details, Skills, …). The Router classifies the query, and the Retriever passes an equality filter to `as_retriever()` so only relevant chunks are returned. |
| **Resume-style Home page** | All content is sourced from `About_me.docx`. Education, experience, and projects are rendered as an interactive timeline; skills are grouped & colour-coded by category. |
| **Session memory** | The last 20 messages are kept in-memory and the last 3 exchanges are fed into the Responder prompt for conversational continuity. |

---

## 🏗️ Project Structure

```
ai_digital_profile/
├── app.py                          # Streamlit app – Home & Chat pages
├── config/
│   ├── __init__.py
│   ├── settings.py                 # All tuneable config (keys, model, paths)
│   └── prompts.py                  # TOPIC_MAP + prompts for every agent node
├── data/
│   ├── About_me.docx               # Source document (used to build the vector store)
│   └── vector_store/               # Pre-built FAISS index + metadata (committed to repo)
├── src/
│   ├── __init__.py
│   ├── rag_engine.py               # Loads FAISS, exposes metadata-filtered retrieve()
│   ├── chatbot.py                  # LangGraph graph definition + ProfileChatbot façade
│   └── ui_components.py            # All CSS & reusable rendering functions
├── assets/
│   └── profile_photo.jpg           # Professional headshot (400×400 px recommended)
├── scripts/
│   ├── setup_vectordb.py           # One-time script to (re-)build the vector store
│   └── test_chatbot.py             # Manual smoke-test of the chatbot
├── tests/
│   ├── test_rag_engine.py          # Unit tests – RAG engine
│   └── test_chatbot.py             # Unit tests – chatbot & graph nodes
├── Dockerfile                      # Container image
├── docker-compose.yml              # Single-command local deployment
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- An OpenAI **or** Google API key
- The pre-built `data/vector_store/` directory already in the repo (no rebuild needed)

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Open .env and set ONE of:
#   OPENAI_API_KEY=sk-...
#   GOOGLE_API_KEY=AIza...
# Optionally override LLM_PROVIDER (default: openai)
```

### 4. Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

> **No `setup_vectordb.py` step is required** — the vector store is pre-built and ships with the repo. Only run that script if you change `About_me.docx` and need to rebuild.

---

## 🤖 Chatbot Architecture (LangGraph)

```
User Query
    │
    ▼
┌──────────┐   off_topic   ┌─────────────┐
│  ROUTER  │ ────────────► │ OFF_TOPIC   │ ► END
└────┬─────┘               └─────────────┘
     │ valid topic
     ▼
┌──────────┐
│RETRIEVER │   metadata filter: {"topic": <topic>}
└────┬─────┘
     │
     ▼
┌───────────┐  INSUFFICIENT   ┌──────────────┐
│ VALIDATOR │ ──────────────► │ INSUFFICIENT │ ► END
└────┬──────┘                 └──────────────┘
     │ SUFFICIENT
     ▼
┌───────────┐
│ RESPONDER │ ► END
└───────────┘
```

### Supported topics (from `TOPIC_MAP` in `config/prompts.py`)

| Topic | What it covers |
|---|---|
| Introduction | Who Vivek is, career overview |
| Family Background | Personal background |
| Education | B.Eng & M.Sc. details |
| Job Summary | TCS, Accenture, Clover roles |
| Project Details | All projects write-ups |
| Skills | AI/ML, programming, data-eng skills |
| Honors and Awards | TCS & Accenture awards |
| Licences and Certifications | Databricks cert, M.Sc. credential |
| Hobbies | What keeps me moving |
| Languages Known | Language than Vivek speaks |
| Weakness | His weaknesses |
| Role Suitability | Why he's the ideal fit |

---

## 📝 Customisation

| What | Where |
|---|---|
| **Profile photo** | Replace `assets/profile_photo.jpg` |
| **Contact links** | Edit `PROFILE_INFO` dict in `config/settings.py` |
| **Profile content** | Edit `data/About_me.docx`, then rebuild: `python scripts/setup_vectordb.py` |
| **LLM / model** | Set `LLM_PROVIDER` and `MODEL_NAME` in `.env` |
| **Colours & layout** | Edit `_CSS` string in `src/ui_components.py` |
| **Agent prompts** | Edit the prompt constants in `config/prompts.py` |
| **Retrieval count** | Set `TOP_K_RESULTS` and `FETCH_RESULTS` in `.env` (default 4 and 10) |

---

## 🧪 Testing

```bash
# Manual chatbot smoke-test (API key required)
python scripts/test_chatbot.py
```

---

## 🐳 Docker

```bash
# Build & run in one command
docker compose up --build
```

The container exposes port **8501**. Secrets are injected via the `.env` file (mapped as a volume in `docker-compose.yml`).

---

## 📊 Deployment Options

| Platform | Cost | Setup time |
|---|---|---|
| **Streamlit Cloud** | Free | ~15 min |
| **Heroku** | $7–25 / mo | ~30 min |
| **AWS EC2** | $10–30 / mo | ~1 hr |
| **Google Cloud Run** | Pay-per-use | ~45 min |

### Streamlit Cloud (recommended)

1. Push the repo to GitHub (make sure `data/vector_store/` is committed).
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → New app → point at `app.py`.
3. Add `OPENAI_API_KEY` (or `GOOGLE_API_KEY`) in **Advanced settings → Secrets**.
4. Click **Deploy**.

---

## 🔐 Security

- **Never** commit `.env`, `data/vector_store`, or raw API keys.
- Use Streamlit Secrets or platform-native secret managers in production.
- The vector store contains only professional profile data — no PII beyond what you choose to include.

---

## 🐛 Troubleshooting

| Symptom | Fix |
|---|---|
| *"Vector store not found"* | Ensure `data/vector_store/` exists. Rebuild with `python scripts/setup_vectordb.py`. |
| *API key error* | Verify `.env` has the correct key and `LLM_PROVIDER` matches. |
| *Router returns wrong topic* | Lower `TEMPERATURE` in `.env` (try `0.3`) for more deterministic routing. |
| *Memory / slow startup* | Reduce `TOP_K_RESULTS` in `.env`. |

---

## 📚 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Agentic AI | LangGraph (StateGraph, conditional edges) |
| LLM Orchestration | LangChain |
| LLM Providers | OpenAI GPT-4o · Google Gemini |
| Vector DB | FAISS (metadata-filtered) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Language | Python 3.9+ |

---

## 📄 License

Personal / portfolio use. Feel free to fork and adapt for your own profile.

---

*Built with LangGraph, LangChain, FAISS, Groq, Nomic AI, and Streamlit.*