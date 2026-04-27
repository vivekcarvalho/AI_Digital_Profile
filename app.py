"""
AI-Powered Digital Profile – Main Streamlit Application
=========================================================
Home page   → resume-style layout (hero → summary → education → experience
              → projects → skills → awards → certs → CTA)
Chat page   → LangGraph agentic chatbot with topic-filtered RAG
"""

import streamlit as st

from config import settings
from src.rag_engine import get_rag_engine
from src.chatbot import ProfileChatbot
from src.ui_components import (
    apply_custom_css,
    render_hero,
    render_section_header,
    render_timeline_card,
    render_skills,
    render_award,
    render_cta,
    render_chat_header,
    render_chat_bubble,
    initialize_session_state,
)

# ---------------------------------------------------------------------------
# Page config (set once, before any other st call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{settings.DEVELOPER_NAME} – AI Profile",
    page_icon="🤖",
    layout="wide",
    # initial_sidebar_state="expanded",
    initial_sidebar_state="auto",
)

# ===========================================================================
# HOME PAGE – every section's data comes from about_me.txt
# ===========================================================================
def render_home():
    apply_custom_css()

    # ── Hero ──────────────────────────────────────────────────────────────
    render_hero(settings.PROFILE_INFO, settings.PROFILE_PICTURE_PATH)

    # ── About / Summary ───────────────────────────────────────────────────
    render_section_header("👤", "About Me")
    st.markdown("""
    <div class="glass-card">
        <p style="font-size:.9rem;color:#475569;line-height:1.75;margin:0;">
            A <strong>Senior Data & AI Specialist</strong> with <strong>15+ years</strong> of hands-on
            experience spanning Data Engineering, Machine Learning, Deep Learning, and cutting-edge
            <strong>Agentic AI Development</strong>. My career journey began in 2011 as a Data Warehouse
            Developer and has evolved into designing and deploying <strong>production-grade AI systems</strong>,
            building <strong>autonomous analytics agents</strong>, and leading enterprise-scale digital
            transformation initiatives across <strong>Banking, Financial Services & Insurance (BFSI)</strong>
            — delivering measurable business value through AI-powered analytics, predictive modelling,
            and intelligent automation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Education ─────────────────────────────────────────────────────────
    render_section_header("🎓", "Education")
    render_timeline_card(
        title="Master of Science – Computer Science (AI & ML)",
        subtitle="Woolf University",
        date="Jul 2024",
        bullets=[
            "Specialised in Production AI Architecture, MLOps, and LLM Engineering.",
            "Advanced coursework: Deep Learning, NLP, Computer Vision, Statistical Modelling.",
            "Hands-on with TensorFlow, Keras, PyTorch, LangChain, LangGraph.",
        ],
    )
    render_timeline_card(
        title="Bachelor of Engineering – Electronics & Telecommunication",
        subtitle="University of Mumbai",
        date="2009",
        bullets=[
            "Strong foundation in C, C++, Python, SQL and RDBMS.",
            "Developed analytical, problem-solving and technical-communication skills.",
        ],
        is_last=True,
    )

    # ── Career Experience ─────────────────────────────────────────────────
    render_section_header("💼", "Career Highlights")
    render_timeline_card(
        title="Tata Consultancy Services (TCS)",
        subtitle="Functional Consultant / Process Expert",
        date="May 2021 – Present",
        bullets=[
            "Lead enterprise AI/ML & advanced analytics for consumer banking & credit-card portfolios.",
            "Architected autonomous AI analyst — 94 % validation confidence, < 10 s query latency.",
            "Built self-serve analytics platform reducing business-analysis time by 60 %.",
            "Partnered with senior leadership to embed AI-driven intelligence into revenue-generating processes.",
        ],
    )
    render_timeline_card(
        title="Accenture",
        subtitle="Analyst → Senior Analyst → Specialist → Associate Project Manager",
        date="Aug 2013 – Apr 2021",
        bullets=[
            "Designed customer-segmentation models driving 42 % growth in cross-product sales.",
            "Architected EDW & ETL solutions during M&A transitions, improving efficiency by 25 %.",
            "Automated KPI tracking reducing delivery timelines by 60 %.",
            "Built automation eliminating ~70 % of manual insurance reporting.",
            "Ensured data governance & regulatory compliance across analytics systems.",
        ],
    )
    render_timeline_card(
        title="Clover Infotech Pvt. Ltd.",
        subtitle="Software Engineer",
        date="Jan 2011 – Aug 2013",
        bullets=[
            "Designed Enterprise Data Warehouse integrating underwriting, claims & reinsurance data.",
            "Automated reporting frameworks, reducing delivery timelines by 50 %.",
            "Delivered P&L and executive KPI dashboards across agent, product & geography dimensions.",
        ],
        is_last=True,
    )

    # ── Featured Projects ─────────────────────────────────────────────────
    render_section_header("🚀", "Featured Projects")

    # --- TCS projects (newest first) ---
    render_timeline_card(
        title="Coding a Multimodal (Vision) Language Model (Google PaliGemma) from Scratch (PyTorch)",
        subtitle="End-to-End Multimodal Transformer Implementation with Vision Encoding, Fusion, and Text Generation",
        date="Apr 2026",
        bullets=[
            "Built a multimodal Vision Language Model (VLM) from scratch in PyTorch, combining a Vision Transformer (ViT) encoder with a Transformer-based language decoder (PaliGemma-style).",
            "Implemented multimodal fusion via projection layers and autoregressive text generation, incorporating concepts from CLIP/SigLip.",
            "Engineered advanced components including rotary positional embeddings, grouped query attention (GQA), and KV-cache for efficient inference.",
            "Successfully integrated and aligned pre-trained Hugging Face weights into the custom architecture for local multimodal inference and validation.",
            "Applied core skills: PyTorch, multimodal LLM architecture, Vision Transformers, Transformer optimization, inference acceleration, model weight integration."
        ],
    )
    render_timeline_card(
        title="GPT-2 LLM from Scratch (PyTorch)",
        subtitle="End-to-End GPT-2 Architecture Implementation with Transformer Blocks and Training Optimization",
        date="Mar 2026",
        bullets=[
            "Built a GPT-2 style Transformer language model from scratch in PyTorch, implementing embeddings, multi-head self-attention, and autoregressive decoding.",
            "Engineered a full training pipeline with cross-entropy loss, AdamW optimization, gradient clipping, and mixed precision training.",
            "Solved key challenges in GPU memory management, loss convergence, and attention masking through low-level debugging and optimization.",
            "Applied core skills: PyTorch, Transformer architecture, LLM engineering, training loop optimization, numerical stability techniques.",
            "Successfully mapped and loaded pre-trained GPT-2 weights into the custom architecture for local inference, validating implementation fidelity."
        ],
    )
    render_timeline_card(
        title="Enterprise Autonomous Data Analyst",
        subtitle="Production Multi-Agent AI System · LangGraph + LLM",
        date="Jan 2026 · TCS",
        bullets=[
            "4 specialised agents with Plan–Act–Observe–Critique loop; 94 % validation confidence, < 10 s latency.",
            "Metadata-intelligence framework analysing 8+ characteristics — hallucinations cut by 80 %.",
            "5 % hallucination rate vs ~25 % industry baseline via multi-layered validation.",
            "Democratised analytics for non-technical users: hours-to-insight → seconds.",
        ],
    )
    render_timeline_card(
        title="Digital Profile with Agentic AI Chatbot & RAG",
        subtitle="Next-Gen Recruiter-Facing AI Platform",
        date="Jan 2026",
        bullets=[
            "RAG system fetching precise context from a curated knowledge base, passed to an LLM for natural-language responses.",
            "Agentic AI architecture reasoning, validating, and orchestrating multiple agents for accurate answers.",
            "Query filtering & relevance checks keep the bot focused on high-value recruiter questions.",
        ],
    )
    render_timeline_card(
        title="AI-Powered Self-Serve Analytics & KPI Insights",
        subtitle="Natural-Language BI Platform",
        date="Jun – Jul 2025 · TCS",
        bullets=[
            "Natural-language query processing pipelines for consumer-banking data.",
            "60 % reduction in business-analysis time (~10 hrs/week saved).",
            "Interactive KPI dashboards with trend alerts and red-flag detection for real-time decisions.",
        ],
    )
    render_timeline_card(
        title="Multi-Language MCQ Generator",
        subtitle="AI-Powered Assessment Tool · LangChain + Google GenAI",
        date="Sep 2024 · TCS",
        bullets=[
            "Up to 30 MCQs per document in 5–7 seconds — ~75 % productivity improvement.",
            "Cognitive & language-quality evaluation ensuring pedagogical soundness.",
            "Language-agnostic framework with multilingual support.",
        ],
    )
    render_timeline_card(
        title="Optimising OTT Recommendation System",
        subtitle="ML-Driven Personalisation Engine",
        date="Jan – Jun 2024 · TCS",
        bullets=[
            "Mitigated content-imbalance bias that was reducing customer growth by ~17 %.",
            "Hybrid collaborative + content-based filtering improved engagement & reduced churn.",
            "Scalable, extensible solution ready for continuous AI/ML enhancements.",
        ],
    )
    render_timeline_card(
        title="Click-Through Rate Enhancement",
        subtitle="Time-Series Analysis & Forecasting · Wikipedia Ad Placements",
        date="Jul – Nov 2023 · TCS",
        bullets=[
            "SARIMAX + Facebook Prophet models on 550 days of visit data; forecasting accuracy up 10 %.",
            "Demographic & language-specific variables tailored ad placement for maximum engagement.",
            "Scalable forecasting framework for AI-driven marketing optimisation.",
        ],
    )
    render_timeline_card(
        title="Graduate Admissions Analysis",
        subtitle="Predictive Modelling · Linear Regression",
        date="May – Jul 2023 · TCS",
        bullets=[
            "Polynomial regression (degree 3) — 96 % test accuracy, 92 % validation accuracy.",
            "Feature-importance analysis across GRE, TOEFL, CGPA, research, SOP & LOR.",
            "Decision-support tool combining interpretability and predictive accuracy.",
        ],
    )
    render_timeline_card(
        title="Student Segmentation for Learning Pathways",
        subtitle="ML-Driven Clustering · K-Means & Hierarchical",
        date="Feb – May 2023 · TCS",
        bullets=[
            "Identified 5 distinct student clusters with targeted career pathways (Innovative Catalysts, Rising Stars, etc.).",
            "Personalised learning interventions and career guidance per cluster.",
            "Scalable segmentation framework supporting continuous updates.",
        ],
    )
    render_timeline_card(
        title="Expansion Strategy for a Renowned Retailer",
        subtitle="Data-Driven Market Analysis · New-Country Entry",
        date="Sep 2022 – Jan 2023 · TCS",
        bullets=[
            "Market-landscape analysis covering demographics, competitors, and e-commerce trends.",
            "Segmentation & predictive analytics to understand consumer behaviour and spending patterns.",
            "Delivered a scalable expansion-planning framework ready for additional markets.",
        ],
    )

    # --- Accenture / Clover legacy projects ---
    render_timeline_card(
        title="Financial Profitability Computation",
        subtitle="Enterprise P&L Framework · Insurance Portfolios",
        date="Apr 2016 – Apr 2021 · Accenture",
        bullets=[
            "Aggregated data across policy inwards, RI outwards, claims, fees, taxes, ELR & IBNR.",
            "Complex computational models for monthly, quarterly, half-yearly & annual profitability.",
            "Supported strategic financial planning, risk assessment & regulatory compliance.",
        ],
    )
    render_timeline_card(
        title="Customer Lifecycle Management (CLM) Analytics",
        subtitle="Centralised Data Warehouse · Insurance",
        date="Aug 2013 – Oct 2016 · Accenture",
        bullets=[
            "Unified view of the entire customer lifecycle from cover-note to current policy status.",
            "Daily ETL pipelines processing high-volume transactional data with full accuracy.",
            "360° policy-lifecycle visibility enabling retention-risk identification.",
        ],
    )
    render_timeline_card(
        title="Finance & Reinsurance Automation",
        subtitle="End-to-End P&L & Reinsurance Workflows",
        date="Oct 2014 – May 2016 · Accenture",
        bullets=[
            "Automated reinsurance treaty-setup generation for accurate obligation computation.",
            "Scalable reporting frameworks for vertical-wise and portfolio-wide financial visibility.",
            "Reduced manual effort and improved accuracy across the enterprise.",
        ],
    )
    render_timeline_card(
        title="Analytics & Data Engineering",
        subtitle="Enterprise Data Warehouse · General Insurance",
        date="Jan 2011 – Aug 2013 · Clover Infotech",
        bullets=[
            "Centralised EDW integrating underwriting, claims, policy, reinsurance & commission data.",
            "PnL computation, reinsurance module integration, automated dashboards & alert systems.",
            "Reduced manual computation & reporting effort by 50 %+.",
        ],
        is_last=True,
    )

    # ── Skills ────────────────────────────────────────────────────────────
    render_section_header("🎯", "Core Skills")
    render_skills({
        "Agentic AI & LLMs": [
            "LangChain", "LangGraph", "LLM Engineering", "Prompt Optimisation",
            "RAG Systems", "Agentic Workflows", "Multi-Agent AI",
            "OpenAI GPT", "Google Gemini", "Groq", "Claude",
        ],
        "ML & Data Science": [
            "Python", "TensorFlow", "Keras", "Scikit-learn",
            "Pandas", "NumPy", "SciPy", "Deep Learning", "NLP",
            "Recommender Systems", "Time-Series Forecasting",
        ],
        "Data Engineering & BI": [
            "SQL", "BigQuery", "Databricks", "Oracle", "Teradata",
            "ETL Pipelines", "Data Architecture", "Tableau", "Power BI", "Streamlit",
        ],
        "DevOps & Practices": [
            "MLOps", "Production AI Architecture", "GitHub",
            "Docker", "FAISS", "Vector Databases",
        ],
    })

    # ── Honours & Awards ──────────────────────────────────────────────────
    render_section_header("🏆", "Honours & Awards")
    render_award("🏆", "gold",
                 "Winner: AI Hackathon – Agentic AI for Sentiment Intelligence – TCS · Feb 2026",
                 "Led the design and delivery of an enterprise-grade Agentic AI Stakeholder Sentiment Intelligence " \
                 "Platform that analyzes multi-channel customer feedback using NLP and autonomous decisioning to " \
                 "generate unbiased insights, identify pain points, and recommend actionable, scalable improvements " \
                 "across business units.")
    render_award("⭐", "gold",
                 "STAR of the Month Award – TCS · Nov 2025",
                 "Recognized for exceptional contribution in architecting and deploying AI-driven analytics solutions " \
                 "that enable stakeholders to independently derive actionable insights through anomaly detection, " \
                 "alerts, and trend analysis, enhancing productivity, reducing analyst dependency, and supporting " \
                 "strategic decision-making; acknowledged by executive leadership as a key innovation and " \
                 "competitive differentiator.")
    render_award("🏅", "gold",
                 "On-The-Spot Award – TCS · Jun 2023",
                 "Awarded for delivering error-free campaign PnL analysis and ensuring regulatory compliance " \
                 "through accurate, adaptive financial reporting, streamlining processes and enabling data-driven " \
                 "decision-making while maintaining high standards of precision and control; recognized for " \
                 "strengthening reporting reliability and supporting business confidence in critical financial insights.")
    render_award("🏅", "gold",
                 "On-The-Spot Award – TCS · Aug 2022",
                 "Acknowledged for driving process improvements and ensuring regulatory submission accuracy, " \
                 "delivering consistent operational excellence and reliable business-critical reporting.")
    render_award("⭐", "gold",
                 "Accenture Celebrate Excellence (ACE) · Nov 2019",
                 "Recognized for delivering innovative, automation-driven analytics solutions that eliminated " \
                 "manual intervention across finance, reinsurance, sales, and marketing, significantly reducing " \
                 "turnaround times and enhancing client value through accurate, precision-led insights.")

    # ── Licences & Certifications ─────────────────────────────────────────
    render_section_header("📜", "Licences & Certifications")
    render_award("📄", "indigo",
                 "Databricks Certified Data Analyst Associate",
                 "Databricks · Oct 2025 – Oct 2027 · Credential ID 163207006")
    render_award("🎓", "indigo",
                 "M.Sc. Computer Science – AI & Machine Learning",
                 "Woolf University · Jul 2024 · Credential ID 324542409")

    # ── Why I'm the Ideal Fit (Role Suitability) ─────────────────────────
    # render_section_header("🎯", "Role Suitability")
    # st.markdown("""
    # <div class="glass-card">
    #     <p style="font-size:.88rem;color:#475569;line-height:1.8;margin:0 0 10px;">
    #         A proven end-to-end AI/ML professional combining <strong>deep technical mastery</strong> with
    #         <strong>business acumen</strong> — architecting and operationalising multi-agent AI systems,
    #         autonomous analysts, and production-grade RAG pipelines using LangGraph, LangChain, and
    #         leading LLMs (GPT, Gemini, Claude, Groq). Hands-on MLOps, prompt optimisation, and
    #         validation-layer expertise ensures robust, low-latency solutions for business-critical processes.
    #     </p>
    #     <p style="font-size:.88rem;color:#475569;line-height:1.8;margin:0 0 10px;">
    #         Delivered measurable impact across <strong>banking, insurance, retail & edtech</strong>: predictive
    #         analytics, customer segmentation, churn forecasting, recommendation systems, and time-series
    #         forecasting driving revenue growth, campaign optimisation, and operational efficiency.
    #     </p>
    #     <p style="font-size:.88rem;color:#475569;line-height:1.8;margin:0;">
    #         Led cross-functional Agile teams, partnering with senior leadership to embed AI-driven
    #         intelligence into decision-making — recognised with <strong>multiple awards</strong> for high-impact
    #         AI products and complex-process automation. Uniquely positioned to contribute at a
    #         <strong>senior AI/ML leadership role</strong>, building innovative, enterprise-ready AI products.
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)

    # ── Call to Action ────────────────────────────────────────────────────
    render_cta()


# ===========================================================================
# CHAT PAGE
# ===========================================================================
# def render_chat():
#     apply_custom_css()

#     render_chat_header(settings.DEVELOPER_NAME)

    # ── Bootstrap chatbot on first visit ──────────────────────────────────
    # if st.session_state.chatbot is None:
    #     with st.spinner("Initialising AI assistant …"):
    #         try:
    #             rag = get_rag_engine()
    #             st.session_state.chatbot = ProfileChatbot(rag)
    #             greeting = st.session_state.chatbot.get_greeting()
    #             st.session_state.chat_history.append({"role": "assistant", "content": greeting})
    #         except Exception as exc:
    #             st.error(f"Could not start chatbot: {exc}")
    #             st.info("Make sure your vector store exists at `data/vector_store/` and your API key is set in `.env`.")
    #             return

    # # ── Render history ────────────────────────────────────────────────────
    # for msg in st.session_state.chat_history:
    #     render_chat_bubble(msg["role"], msg["content"])

    # # ── Input row ─────────────────────────────────────────────────────────
    # col_input, col_send = st.columns([5, 1], gap="small")
    # with col_input:
    #     user_input = st.text_input(
    #         label="Chat Input",
    #         placeholder="e.g. Tell me about your LangGraph projects …",
    #         key="user_input",
    #         label_visibility="collapsed",
    #     )
    # with col_send:
    #     send = st.button("Send", width='stretch')

    # # ── Process ───────────────────────────────────────────────────────────
    # if send and user_input:
    #     st.session_state.chat_history.append({"role": "user", "content": user_input})
    #     with st.spinner("Thinking …"):
    #         reply = st.session_state.chatbot.chat(user_input)
    #     st.session_state.chat_history.append({"role": "assistant", "content": reply})
    #     st.rerun()

    # # ── Clear ─────────────────────────────────────────────────────────────
    # st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    # if st.button("🗑️ Clear Chat", help="Reset the conversation"):
    #     st.session_state.chat_history.clear()
    #     if st.session_state.chatbot:
    #         st.session_state.chatbot.clear_history()
    #         greeting = st.session_state.chatbot.get_greeting()
    #         st.session_state.chat_history.append({"role": "assistant", "content": greeting})
    #     st.rerun()

def clear_chat():
    st.session_state.chat_history.clear()
    if st.session_state.chatbot:
        st.session_state.chatbot.clear_history()
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.chat_history.append(
            {"role": "assistant", "content": greeting}
        )
    st.rerun()

def render_chat():
    apply_custom_css()
    # render_chat_header(settings.DEVELOPER_NAME)
    col_title, col_clear = st.columns([6, 1])
    with col_title:
        render_chat_header(settings.DEVELOPER_NAME)
    with col_clear:
        # if st.button("🗑️ Clear", help="Reset the conversation"):
        #     clear_chat()
        with st.sidebar:
            st.header("Chat Controls")
            if st.button("🗑️ Clear Chat"):
                clear_chat()

    # ── Bootstrap chatbot on first visit ──────────────────────────────────
    if st.session_state.chatbot is None:
        st.empty()
        with st.spinner("Initialising AI assistant …"):
            try:
                rag = get_rag_engine()
                st.session_state.chatbot = ProfileChatbot(rag)
                greeting = st.session_state.chatbot.get_greeting()
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": greeting}
                )
            except Exception as exc:
                st.error(f"Could not start chatbot: {exc}")
                st.info(
                    "Make sure your vector store exists at `data/vector_store/` "
                    "and your API key is set in `.env`."
                )
                return

    # ── Render chat history (ONCE) ────────────────────────────────────────
    AVATARS = {
    "user": "🧑‍💻",
    "assistant": "🤖",
    # "assistant": "🧠",
    # "assistant": "media/profile_pic.jpeg"
    }

    for msg in st.session_state.chat_history:
        # with st.chat_message(msg["role"]):
        #     st.markdown(msg["content"])
        with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
            st.markdown(msg["content"])

    # ── Chat input (Enter to send, Shift+Enter = newline) ─────────────────
    user_input = st.chat_input(
        "e.g. Tell me about your Agentic AI projects …"
    )

    if user_input:
        # 1️⃣ Immediately render user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # 2️⃣ Persist user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        # 3️⃣ Generate & render assistant reply
        with st.chat_message("assistant"):
            with st.spinner("Thinking …"):
                reply = st.session_state.chatbot.chat(user_input)
                st.markdown(reply)

        # 4️⃣ Persist assistant reply
        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )

    # ── Clear chat ────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

    # if st.button("🗑️ Clear Chat", help="Reset the conversation"):
    #     st.session_state.chat_history.clear()

    #     if st.session_state.chatbot:
    #         st.session_state.chatbot.clear_history()
    #         greeting = st.session_state.chatbot.get_greeting()
    #         st.session_state.chat_history.append(
    #             {"role": "assistant", "content": greeting}
    #         )

        # st.rerun()


# ===========================================================================
# MAIN – navigation & sidebar
# ===========================================================================
def main():
    initialize_session_state()

    # ── Dark sidebar nav ──────────────────────────────────────────────────
    # st.sidebar.markdown("## 🗂️ Navigation", unsafe_allow_html=False)
    # page = st.sidebar.radio("", ["🏠  Home", "🤖  AI Chatbot"], key="nav")
    col1, col2 = st.columns([10, 2])
    with col2:
        ai_chat = st.toggle("Ask me Anything",)

    if ai_chat:
        # render_chat()
        page = "Chatbot"
    else:
        # render_home()
        page = "Home"

    st.session_state.current_page = page

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About This Site", unsafe_allow_html=False)
    st.sidebar.info(
        "An AI-powered digital profile showcasing agentic AI via a "
        "LangGraph multi-agent chatbot with topic-filtered RAG retrieval."
    )

    st.sidebar.markdown("### 🛠️ Tech Stack", unsafe_allow_html=False)
    st.sidebar.markdown(
        "**Frontend** · Streamlit\n\n"
        "**Agentic AI** · LangGraph + LangChain\n\n"
        "**LLM** · OpenAI GPT-4o / Google Gemini/ Groq\n\n"
        "**Vector DB** · FAISS (metadata-filtered)\n\n"
        "**Language** · Python 3.9+"
    )

    # ── Route ─────────────────────────────────────────────────────────────

    if "Home" in page:
        render_home()
    else:
        if st.session_state.chatbot is None:
            st.empty()
        render_chat()

if __name__ == "__main__":
    main()