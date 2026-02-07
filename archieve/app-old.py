"""
AI-Powered Digital Profile Website
Main Streamlit Application
"""
import streamlit as st
from src.rag_engine import get_rag_engine
from src.chatbot import ProfileChatbot
from src.ui_components import (
    apply_custom_css,
    render_profile_header,
    render_contact_links,
    render_skills_section,
    create_section,
    render_chat_message,
    initialize_session_state
)
from config import settings


# Page configuration
st.set_page_config(
    page_title=f"{settings.DEVELOPER_NAME} - AI Profile",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_home_page():
    """Render the home/profile page"""
    
    # Apply custom CSS
    apply_custom_css()
    
    # Profile header
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    render_profile_header(settings.PROFILE_INFO, "assets/profile_photo.jpg")
    
    # Contact links
    render_contact_links(settings.PROFILE_INFO)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # About Section
    create_section("👨‍💼 About Me", f"""
        I am **{settings.DEVELOPER_NAME}**, a Senior **Data and AI Specialist** with **14+ years** of experience spanning 
        Data Engineering, Machine Learning, Deep Learning, and cutting-edge **Agentic AI Development**. 
        
        My career journey began in **2011** as a Data Warehouse Developer and has evolved to designing and deploying 
        **production-grade AI systems**, building **autonomous analytics agents**, and leading enterprise-scale digital 
        transformation initiatives.
        
        Based in **Mumbai**, I've delivered high-impact solutions across **Banking, Financial Services, and Insurance (BFSI)**, 
        driving measurable business value through AI-powered analytics, predictive modeling, and intelligent automation.
    """)
    
    # Education
    create_section("🎓 Education", """
        **Master of Science in Computer Science (AI & Machine Learning)**  
        *Woolf University (2024)*  
        - Specialized in Production AI Architecture, MLOps, LLM Engineering  
        - Advanced coursework: Deep Learning, NLP, Computer Vision, Statistical Modeling  
        - Hands-on: TensorFlow, Keras, PyTorch, LangChain, LangGraph
        
        **Bachelor of Engineering (Electronics & Telecommunication)**  
        *University of Mumbai (2009)*  
        - Foundation in programming (C, C++, Python), SQL, RDBMS  
        - Strong technical communication and problem-solving skills
    """)
    
    # Experience Highlights
    create_section("💼 Career Highlights", """
        **Tata Consultancy Services (TCS)** | *May 2021 - Present*  
        *Functional Consultant / Process Expert*
        - Lead enterprise AI/ML and analytics for consumer banking portfolios  
        - Architected autonomous AI analyst with 94% validation confidence and <10s latency  
        - Built self-serve analytics platforms, reducing analysis time by 60%
        
        **Accenture** | *Aug 2013 - Apr 2021*  
        *Associate Project Manager → Application Development Specialist*
        - Progressed through multiple roles in data platforms and advanced analytics  
        - Designed customer segmentation models improving sales by 42%  
        - Led M&A data transitions and platform modernization initiatives  
        - Built automation eliminating 70% of manual insurance reporting
        
        **Clover Infotech** | *Jan 2011 - Aug 2013*  
        *Software Engineer*
        - Designed Enterprise Data Warehouse for insurance analytics  
        - Automated reporting reducing delivery timelines by 50%  
        - Foundation in data architecture and ETL optimization
    """)
    
    # Key Projects
    create_section("🚀 Featured Projects", """
        **1. Enterprise Autonomous Data Analyst (Jan 2026)**  
        Production multi-agent AI system using LangGraph + LLM
        - 4 specialized agents with Plan-Act-Observe-Critique loop  
        - 94% validation confidence, 5% hallucination rate  
        - Democratized analytics for non-technical users
        
        **2. AI-Powered Self-Serve Analytics (Jun-Jul 2025)**  
        Natural language query platform for banking data
        - 60% reduction in analysis time  
        - Interactive KPI dashboards with predictive insights  
        - Real-time trend alerts and anomaly detection
        
        **3. OTT Recommendation System Optimization (Jan-Jun 2024)**  
        ML-driven personalization engine
        - Addressed 17% bias reducing customer growth  
        - Hybrid collaborative + content-based filtering  
        - Improved engagement and reduced churn
        
        **4. Multi-Language MCQ Generator (Sep 2024)**  
        AI-powered assessment creation tool
        - LangChain + Google Generative AI  
        - 75% productivity improvement  
        - Multilingual support with quality evaluation
    """)
    
    # Core Skills
    skills = [
        "Python", "LangChain", "LangGraph", "LLM Engineering",
        "RAG Systems", "OpenAI GPT", "Google Gemini", "Agentic AI",
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", 
        "Keras", "Scikit-learn", "Pandas", "NumPy",
        "FAISS", "Vector Databases", "Streamlit", "MLOps",
        "SQL", "BigQuery", "Databricks", "Tableau", "Power BI",
        "Data Engineering", "ETL", "Data Architecture"
    ]
    render_skills_section(skills)
    
    # Awards & Recognition
    create_section("🏆 Awards & Recognition", """
        - **On-The-Spot Award** (Nov 2025) - AI-driven analytics products deployment  
        - **On-The-Spot Award** (Jun 2023) - Error-free campaign performance analysis  
        - **On-The-Spot Award** (Aug 2022) - Process improvement excellence  
        - **Accenture Celebrate Excellence (ACE)** (Nov 2019) - Analytics automation innovation
    """)
    
    # Certifications
    create_section("📜 Certifications", """
        - **Databricks Certified Data Analyst Associate** (Oct 2025)  
        - **M.Sc. Computer Science: AI & ML** - Woolf University (Jul 2024)
    """)
    
    # Call to Action
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             border-radius: 15px; color: white;'>
            <h2>💬 Want to Learn More?</h2>
            <p style='font-size: 1.2rem;'>Try the AI-powered chatbot to ask specific questions about my experience, 
            projects, or skills!</p>
        </div>
    """, unsafe_allow_html=True)


def render_chat_page():
    """Render the AI chatbot page"""
    
    apply_custom_css()
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.title("🤖 AI Assistant")
    st.markdown(f"""
        Ask me anything about **{settings.DEVELOPER_NAME}'s** experience, skills, projects, or background!  
        I'm powered by RAG (Retrieval-Augmented Generation) for accurate, context-aware responses.
    """)
    
    # Initialize chatbot if not already done
    if st.session_state.chatbot is None:
        try:
            with st.spinner("Initializing AI assistant..."):
                rag_engine = get_rag_engine()
                st.session_state.chatbot = ProfileChatbot(rag_engine)
                # Get greeting
                greeting = st.session_state.chatbot.get_greeting()
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": greeting
                })
        except Exception as e:
            st.error(f"Error initializing chatbot: {str(e)}")
            st.info("Please ensure vector database is set up. Run: `python scripts/setup_vectordb.py`")
            return
    
    # Display chat history
    for message in st.session_state.chat_history:
        render_chat_message(
            role=message["role"],
            content=message["content"],
            avatar=settings.CHATBOT_AVATAR if message["role"] == "assistant" else settings.USER_AVATAR
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your question:",
            key="user_input",
            placeholder="e.g., Tell me about your experience with LangChain and LangGraph..."
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    # Process input
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get bot response
        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.chat(user_input)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Rerun to update chat display
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        if st.session_state.chatbot:
            st.session_state.chatbot.clear_history()
            # Add greeting again
            greeting = st.session_state.chatbot.get_greeting()
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": greeting
            })
        st.rerun()


def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("🗂️ Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["Home", "AI Chatbot"],
        key="nav_radio"
    )
    
    st.session_state.current_page = page
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About This Site")
    st.sidebar.info(
        "This is an AI-powered digital profile showcasing advanced "
        "RAG-based conversational AI, built entirely with Streamlit, "
        "LangChain, and LangGraph."
    )
    
    st.sidebar.markdown("### 🛠️ Tech Stack")
    st.sidebar.markdown("""
        - **Frontend**: Streamlit  
        - **AI/ML**: LangChain, LangGraph  
        - **LLM**: OpenAI GPT / Google Gemini  
        - **Vector DB**: FAISS  
        - **Python**: 3.9+
    """)
    
    # Render selected page
    if page == "Home":
        render_home_page()
    else:
        render_chat_page()


if __name__ == "__main__":
    main()