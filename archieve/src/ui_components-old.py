"""
UI Components and helper functions for Streamlit
"""
import streamlit as st
from typing import Dict
from config import settings


def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
        <style>
        /* Main container */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
        }
        
        /* Profile card */
        .profile-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        }
        
        /* Profile header */
        .profile-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .profile-name {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        
        .profile-title {
            font-size: 1.3rem;
            color: #667eea;
            font-weight: 500;
            margin-bottom: 1rem;
        }
        
        .profile-location {
            font-size: 1rem;
            color: #718096;
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2d3748;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
        }
        
        /* Content sections */
        .content-section {
            background: #f7fafc;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 4px solid #667eea;
        }
        
        /* Skills tags */
        .skill-tag {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            margin: 0.3rem;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        /* Contact links */
        .contact-link {
            display: inline-block;
            background: #48bb78;
            color: white;
            padding: 0.7rem 1.5rem;
            border-radius: 10px;
            margin: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .contact-link:hover {
            background: #38a169;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Chat container */
        .chat-container {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-height: 500px;
        }
        
        /* Chat messages */
        .user-message {
            background: #e6f3ff;
            border-radius: 15px;
            padding: 1rem;
            margin: 0.5rem 0;
            margin-left: 2rem;
        }
        
        .bot-message {
            background: #f0f4f8;
            border-radius: 15px;
            padding: 1rem;
            margin: 0.5rem 0;
            margin-right: 2rem;
        }
        
        /* Buttons */
        .stButton>button {
            background: #667eea;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.7rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Input field */
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            padding: 0.7rem;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Responsive image */
        .profile-image {
            border-radius: 50%;
            border: 5px solid #667eea;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)


def render_profile_header(profile_info: Dict, image_path: str = None):
    """
    Render profile header with photo and basic info
    
    Args:
        profile_info: Dictionary with profile information
        image_path: Path to profile photo
    """
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if image_path:
            try:
                st.image(image_path, width=250, use_column_width=False)
            except:
                st.write("📸 Photo not available")
    
    with col2:
        st.markdown(f"""
            <div class="profile-header">
                <h1 class="profile-name">{profile_info.get('name', 'Profile')}</h1>
                <p class="profile-title">{profile_info.get('title', '')}</p>
                <p class="profile-location">📍 {profile_info.get('location', '')}</p>
            </div>
        """, unsafe_allow_html=True)


def render_contact_links(profile_info: Dict):
    """
    Render contact links
    
    Args:
        profile_info: Dictionary with contact information
    """
    st.markdown("### 📫 Contact & Links")
    
    links_html = "<div style='text-align: center;'>"
    
    if profile_info.get('email'):
        links_html += f"""
            <a href="mailto:{profile_info['email']}" class="contact-link">
                📧 Email
            </a>
        """
    
    if profile_info.get('linkedin'):
        links_html += f"""
            <a href="{profile_info['linkedin']}" target="_blank" class="contact-link">
                💼 LinkedIn
            </a>
        """
    
    if profile_info.get('github'):
        links_html += f"""
            <a href="{profile_info['github']}" target="_blank" class="contact-link">
                🔗 GitHub
            </a>
        """
    
    if profile_info.get('portfolio'):
        links_html += f"""
            <a href="{profile_info['portfolio']}" target="_blank" class="contact-link">
                🌐 Portfolio
            </a>
        """
    
    links_html += "</div>"
    
    st.markdown(links_html, unsafe_allow_html=True)


def render_skills_section(skills: list):
    """
    Render skills as tags
    
    Args:
        skills: List of skills
    """
    st.markdown('<div class="section-header">🎯 Core Skills</div>', unsafe_allow_html=True)
    
    skills_html = "<div style='text-align: center;'>"
    for skill in skills:
        skills_html += f'<span class="skill-tag">{skill}</span>'
    skills_html += "</div>"
    
    st.markdown(skills_html, unsafe_allow_html=True)


def render_chat_message(role: str, content: str, avatar: str = None):
    """
    Render a chat message
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        avatar: Avatar image or emoji
    """
    if role == "user":
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
                <div class="user-message">
                    {content}
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(avatar if avatar else "👤")
    else:
        col1, col2 = st.columns([1, 4])
        with col1:
            if avatar and avatar.endswith(('.jpg', '.png', '.jpeg')):
                try:
                    st.image(avatar, width=50)
                except:
                    st.write("🤖")
            else:
                st.write(avatar if avatar else "🤖")
        with col2:
            st.markdown(f"""
                <div class="bot-message">
                    {content}
                </div>
            """, unsafe_allow_html=True)


def create_section(title: str, content: str):
    """
    Create a content section
    
    Args:
        title: Section title
        content: Section content (Markdown supported)
    """
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-section">{content}</div>', unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"