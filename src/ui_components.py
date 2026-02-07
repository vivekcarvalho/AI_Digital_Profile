"""
UI Components – every visual element the app renders.

Design language:
  • Dark sidebar (#0f172a) + crisp white content area
  • Accent colour: indigo-500 (#6366f1) with a violet shift on hover (#7c3aed)
  • Glassmorphism cards with a subtle backdrop blur
  • Timeline dots for experience/project rows
  • Skill pills grouped by category with distinct accent colours
  • Chat bubbles: user → right-aligned indigo, bot → left-aligned slate
"""

import streamlit as st
import streamlit.components.v1 as components

from typing import Dict


# ---------------------------------------------------------------------------
# Master stylesheet – injected once per page render
# ---------------------------------------------------------------------------
_CSS = """
<style>
/* ===== GLOBAL ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .main, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background: #f0f4f8;
    color: #1e293b;
}

/* hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f1f5f9 !important;
    border-bottom: 1px solid #334155;
    padding-bottom: 6px;
    margin-bottom: 10px;
}
/* radio buttons */
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-weight: 500;
    font-size: 0.95rem;
}
[data-testid="stSidebar"] .stRadio input:checked + label {
    color: #a5b4fc !important;
}

/* ===== HERO CARD ===== */
.hero-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 24px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(0,0,0,.18);
    display: flex;
    align-items: center;
    gap: 2.4rem;
}
.hero-photo {
    width: 160px; height: 160px;
    border-radius: 50%;
    border: 4px solid #6366f1;
    box-shadow: 0 0 24px rgba(99,102,241,.35);
    object-fit: cover;
    flex-shrink: 0;
}
.hero-photo-placeholder {
    width: 160px; height: 160px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 3.2rem;
    flex-shrink: 0;
    box-shadow: 0 0 24px rgba(99,102,241,.35);
}
.hero-text { flex: 1; }
.hero-name {
    font-size: 2.2rem; font-weight: 800;
    color: #f1f5f9; margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.hero-title {
    font-size: 1.05rem; font-weight: 500;
    color: #a5b4fc; margin: 0 0 10px;
}
.hero-loc {
    font-size: 0.88rem; color: #64748b;
    margin: 0;
}
.hero-loc span { color: #6366f1; margin-right: 6px; }

/* ===== CONTACT PILLS ===== */
.contact-row {
    display: flex; flex-wrap: wrap; gap: 10px;
    justify-content: center;
    margin: 1.6rem 0 0.4rem;
}
.contact-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(99,102,241,.12);
    border: 1px solid rgba(99,102,241,.25);
    color: #a5b4fc;
    padding: 8px 18px;
    border-radius: 50px;
    text-decoration: none;
    font-size: 0.82rem; font-weight: 600;
    transition: all .25s ease;
    white-space: nowrap;
}
.contact-pill:hover {
    background: #6366f1;
    color: #fff;
    border-color: #6366f1;
    box-shadow: 0 4px 14px rgba(99,102,241,.4);
    transform: translateY(-2px);
}

/* ===== SECTION HEADER ===== */
.sec-header {
    display: flex; align-items: center; gap: 12px;
    margin: 2.2rem 0 1rem;
}
.sec-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.sec-title {
    font-size: 1.25rem; font-weight: 700;
    color: #1e293b; margin: 0;
}

/* ===== GLASS CARD ===== */
.glass-card {
    background: rgba(255,255,255,.92);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(99,102,241,.12);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,.06);
}

/* ===== TIMELINE ROW (experience / project) ===== */
.tl-row {
    display: flex; gap: 1rem; align-items: flex-start;
    margin-bottom: 1rem;
}
.tl-dot-wrap {
    display: flex; flex-direction: column; align-items: center;
    flex-shrink: 0; width: 18px;
}
.tl-dot {
    width: 16px; height: 16px;
    border-radius: 50%;
    background: #6366f1;
    border: 3px solid #fff;
    box-shadow: 0 0 0 3px #6366f1;
    flex-shrink: 0;
}
.tl-line {
    width: 3px; flex: 1; min-height: 30px;
    background: linear-gradient(to bottom, #6366f1, #c7d2fe);
    border-radius: 2px; margin-top: 4px;
}
.tl-line.last {
    background: transparent;
}
.tl-card {
    flex: 1;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,.04);
    transition: box-shadow .2s;
}
.tl-card:hover { box-shadow: 0 6px 24px rgba(99,102,241,.12); }
.tl-company {
    font-size: 1rem; font-weight: 700; color: #1e293b;
    margin: 0 0 2px;
}
.tl-role {
    font-size: 0.82rem; color: #6366f1; font-weight: 600;
    margin: 0 0 4px;
}
.tl-date {
    font-size: 0.75rem; color: #94a3b8; font-weight: 500;
    margin: 0 0 6px;
    display: inline-block;
    background: #f1f5f9; border-radius: 20px; padding: 2px 10px;
}
.tl-bullet { margin: 4px 0 0 12px; font-size: 0.82rem; color: #475569; line-height: 1.55; }
.tl-bullet li { list-style: none; position: relative; padding-left: 16px; }
.tl-bullet li::before {
    content: "›"; position: absolute; left: 0; color: #6366f1; font-weight: 700;
}

/* ===== SKILL PILLS ===== */
.skill-group-title {
    font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #94a3b8; margin: 1rem 0 6px;
}
.skill-pills { display: flex; flex-wrap: wrap; gap: 7px; }
.skill-pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 0.78rem; font-weight: 600;
    border: 1px solid;
    transition: transform .18s, box-shadow .18s;
}
.skill-pill:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,.12); }
/* colour variants */
.sp-indigo  { background:#eef2ff; color:#4f46e5; border-color:#c7d2fe; }
.sp-violet { background:#f5f3ff; color:#7c3aed; border-color:#ddd6fe; }
.sp-emerald { background:#ecfdf5; color:#059669; border-color:#a7f3d0; }
.sp-rose    { background:#fff1f2; color:#e11d48; border-color:#fda4af; }
.sp-amber   { background:#fffbeb; color:#d97706; border-color:#fcd34d; }
.sp-teal     { background:#ecfafa; color:#3B8C8A; border-color:#5eead4; }
.sp-slate    { background:#f1f5f9; color:#5A7D9A; border-color:#cbd5e1; }
.sp-peach    { background:#fff5eb; color:#E7BFA1; border-color:#ffd8b5; }
.sp-lavender { background:#f8f4ff; color:#BFA0E2; border-color:#ddd6fe; }

/* ===== AWARD / CERT ROW ===== */
.award-row {
    display: flex; gap: 12px; align-items: flex-start;
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 1rem 1.2rem;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
}
.award-badge {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; flex-shrink: 0;
}
.award-badge.gold   { background: #fef3c7; }
.award-badge.indigo { background: #eef2ff; }
.award-text h4 { margin: 0 0 2px; font-size: 0.88rem; color: #1e293b; font-weight: 700; }
.award-text p  { margin: 0;    font-size: 0.76rem; color: #64748b; }

/* ===== CTA BANNER ===== */
.cta-banner {
    background: linear-gradient(135deg, #6366f1, #7c3aed);
    border-radius: 20px;
    padding: 2rem 2.4rem;
    text-align: center;
    margin-top: 2.4rem;
    box-shadow: 0 8px 30px rgba(99,102,241,.3);
}
.cta-banner h2 { color:#fff; font-size:1.5rem; margin:0 0 8px; }
.cta-banner p  { color:#c7d2fe; font-size:0.92rem; margin:0; }

/* ===== CHAT PAGE ===== */
.chat-header {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-radius: 20px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 24px rgba(0,0,0,.15);
}
.chat-header h2 { color:#f1f5f9; font-size:1.4rem; margin:0 0 4px; }
.chat-header p  { color:#94a3b8; font-size:0.82rem; margin:0; }

.chat-bubble {
    display: flex; align-items: flex-start; gap: 10px;
    margin-bottom: 14px;
}
.chat-bubble.user { flex-direction: row-reverse; }

.bubble-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
}
.bubble-avatar.bot  { background: linear-gradient(135deg, #6366f1, #7c3aed); color:#fff; }
.bubble-avatar.user { background: #e2e8f0; color:#475569; }

.bubble-text {
    max-width: 78%;
    padding: 10px 16px;
    border-radius: 16px;
    font-size: 0.84rem;
    line-height: 1.6;
    word-wrap: break-word;
}
.bubble-text.bot  { background:#fff; border:1px solid #e2e8f0; color:#1e293b; box-shadow: 0 2px 8px rgba(0,0,0,.06); }
.bubble-text.user { background:#6366f1; color:#fff; border:1px solid #6366f1; }

/* chat input row */
.chat-input-row {
    display: flex; gap: 10px; margin-top: 1rem; align-items: center;
}
.chat-input-row input {
    flex:1; border-radius:50px; border:2px solid #e2e8f0;
    padding: 10px 20px; font-size:0.85rem; font-family:'Inter',sans-serif;
    outline:none; transition: border-color .2s;
}
.chat-input-row input:focus { border-color:#6366f1; }

/* Streamlit widget overrides */
.stButton>button {
    background: #6366f1 !important; color:#fff !important;
    border: none !important; border-radius: 50px !important;
    padding: 8px 22px !important; font-weight: 600 !important;
    font-size: 0.82rem !important; font-family: 'Inter',sans-serif !important;
    transition: all .22s !important; cursor: pointer;
}
.stButton>button:hover {
    background: #4f46e5 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,.4) !important;
    transform: translateY(-1px) !important;
}
.stTextInput>div>div>input {
    border-radius: 50px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 9px 18px !important;
    font-family: 'Inter',sans-serif !important;
    font-size: 0.84rem !important;
    outline: none !important;
}
.stTextInput>div>div>input:focus { border-color: #6366f1 !important; }

/* =======================================================
   RESPONSIVE ADJUSTMENTS 
   ======================================================= */

/* -------- Tablets & small laptops -------- */
@media (max-width: 1024px) {

    .hero-card {
        padding: 2rem;
        gap: 1.6rem;
    }

    .hero-name {
        font-size: 1.9rem;
    }

    .bubble-text {
        max-width: 85%;
    }
}

/* -------- Phones & narrow screens -------- */
@media (max-width: 768px) {

    /* Stack hero layout */
    .hero-card {
        flex-direction: column;
        text-align: center;
    }

    .hero-photo,
    .hero-photo-placeholder {
        width: 120px;
        height: 120px;
    }

    .hero-name {
        font-size: 1.6rem;
    }

    .hero-title {
        font-size: 0.95rem;
    }

    /* Contact pills center nicely */
    .contact-row {
        justify-content: center;
    }

    /* Timeline spacing */
    .tl-row {
        gap: 0.7rem;
    }

    .tl-card {
        padding: 1rem;
    }

    /* Chat bubbles become wider */
    .bubble-text {
        max-width: 92%;
        font-size: 0.82rem;
    }

    /* Section headers breathe better */
    .sec-header {
        margin-top: 1.6rem;
    }

    /* CTA banner */
    .cta-banner {
        padding: 1.6rem;
    }

    .cta-banner h2 {
        font-size: 1.25rem;
    }

    .chat-input-row {
        flex-direction: column;
        gap: 8px;
    }

    .chat-input-row input,
    .stButton > button {
        width: 100%;
    }

    [data-testid="stSidebar"] {
        min-width: 260px;
    }
}

/* -------- Very small phones -------- */
@media (max-width: 480px) {

    .hero-name {
        font-size: 1.4rem;
    }

    .hero-title {
        font-size: 0.9rem;
    }

    .skill-pill {
        font-size: 0.72rem;
        padding: 4px 12px;
    }

    .bubble-avatar {
        width: 28px;
        height: 28px;
        font-size: 0.9rem;
    }
}

</style>
"""


def apply_custom_css():
    """Inject the master stylesheet exactly once."""
    st.markdown(_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Hero / header card
# ---------------------------------------------------------------------------
def render_hero(profile_info: Dict, image_path: str | None = None):
    """Dark hero card: photo (or gradient placeholder) + name / title / location + contact pills."""

    cta_style = """
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        background: linear-gradient(135deg,#1e293b,#0f172a); /* final background */
        border: 1px solid rgba(99,102,241,0.7);           /* final border */
        color: #a5b4fc;                                     /* final text color */
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.05em;                             /* added subtle spacing */
        transition: all 0.2s ease;
        backdrop-filter: blur(8px);
        white-space: nowrap;
    """

    CONTACT_CTA_CSS = """
        <style>
        .contact-pill {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 0.4rem 1.2rem;
            border-radius: 999px;
            background: rgba(148, 163, 184, 0.15);
            border: 1px solid rgba(148, 163, 184, 0.3);
            color: #cbd5e1;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 500;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
            white-space: nowrap;
        }

        .contact-pill:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 24px rgba(99,102,241,.35);
            border-color: rgba(99,102,241,.7);
            color: #a5b4fc;
        }
        </style>
        """

    info = profile_info

    # Clean WhatsApp number for the URL
    if info.get("whatsapp"):
        wa_num = ''.join(filter(str.isdigit, info["whatsapp"]))

    # Clean Mobile number for the URL
    if info.get("mobile"):
        phone_clean = ''.join(filter(str.isdigit, info["mobile"]))

    url_html_tags = []
   
    icon_email = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="auto" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>'
    icon_linkedin = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="auto" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>'
    icon_github = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="auto" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'
    icon_web = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="auto" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    icon_whatsapp = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="auto" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.438 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>'
    icon_phone = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="auto" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>'

        # Layout HTML for Whatsapp and Mobile
    if info.get("whatsapp") and info.get("mobile"):
        contact_html = f"""
        <div style="display: flex; flex-direction: column; align-items: flex-end; width: 100%;">
            <a href="https://wa.me/{wa_num}" target="_blank" class= "contact-pill" style="{cta_style}">
                {icon_whatsapp} <span>WhatsApp</span>
            </a><br>
            <a href="tel:{phone_clean}" class= "contact-pill" style="{cta_style}">
                {icon_phone} <span>Mobile No</span>
            </a>
        </div>
        """
    else:
        contact_html = """<div></div>"""

    if info.get("email"):
        url_html_tags.append(f'<a href="mailto:{info["email"]}" class="contact-pill" style="{cta_style}">{icon_email} Email</a>')
    if info.get("linkedin"):
        url_html_tags.append(f'<a href="{info["linkedin"]}" target="_blank" class="contact-pill" style="{cta_style}">{icon_linkedin} LinkedIn</a>')
    if info.get("github"):
        url_html_tags.append(f'<a href="{info["github"]}" target="_blank" class="contact-pill" style="{cta_style}">{icon_github} GitHub</a>')
    if info.get("portfolio"):
        url_html_tags.append(f'<a href="{info["portfolio"]}" target="_blank" class="contact-pill" style="{cta_style}">{icon_web} Portfolio</a>')

    url_html = '<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 2rem; justify-content: center;">' + "\n".join(url_html_tags) + '</div>'

    # Two-column layout so st.image works for the photo
    col_photo, col_text = st.columns([1, 3], gap="medium")

    with col_photo:
        # st.markdown('<div style="background:#0f172a;border-radius:24px;padding:1.6rem 0.8rem;display:flex;align-items:center;justify-content:center;height:100%;">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if image_path:
            try:
                # st.image(image_path, width='content')
                st.image(image_path, width=215)
            except Exception:
                st.markdown('<div class="hero-photo-placeholder">👤</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hero-photo-placeholder">👤</div>', unsafe_allow_html=True)
        # st.markdown('</div>', unsafe_allow_html=True)

    with col_text:

        components.html(
            f"""
            {CONTACT_CTA_CSS}
            <div style="
                min-height:260px;
                height:auto;
                background:linear-gradient(135deg,#1e293b,#0f172a);
                border:1px solid rgba(255,255,255,0.1);
                border-radius:24px;
                padding:1.8rem 2rem;
                box-shadow:0 10px 12px rgba(0,0,0,.5);
                color:#f8fafc;
                font-family:'Inter',sans-serif;">

                <!-- Top Row: Name + Contact Stack -->
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:24px;">

                    <!-- Identity -->
                    <div style="flex:1;">
                        <h1 style="
                            margin:0;
                            font-size:2.5rem;
                            font-weight:800;
                            color:#ffffff;
                            text-shadow:0 6px 7px rgba(0,255,255,.5);">
                            {info.get('name','')}
                        </h1>

                        <p style="
                            margin:0.5rem 0 0.25rem 0;
                            font-size:1.1rem;
                            font-weight:500;
                            letter-spacing:0.09em;
                            color:#cbd5f5;">
                            {info.get('title','')}
                        </p>

                        <p style="margin:0; color:#EDE8E8; letter-spacing:0.05em;">
                            📍 {info.get('location','')}
                        </p>
                    </div>

                    <!-- Direct Contact (Phone / WhatsApp) -->
                    <div>
                        {contact_html}
                    </div>

                </div>
                
                <!-- Primary CTA row -->
                <div style="margin-top:1.6rem;">
                    {url_html}
                </div>

            </div>
            """,
            height=320,  # safe default
            scrolling=False,
        )

# ---------------------------------------------------------------------------
# Section header (icon + title)
# ---------------------------------------------------------------------------
def render_section_header(icon: str, title: str):
    st.markdown(f"""
    <div class="sec-header">
        <div class="sec-icon">{icon}</div>
        <h2 class="sec-title">{title}</h2>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Timeline card – one experience or project entry
# ---------------------------------------------------------------------------
def render_timeline_card(title: str, subtitle: str, date: str, bullets: list[str], is_last: bool = False):
    """
    title    – company or project name
    subtitle – role or one-line description
    date     – e.g. "May 2021 – Present"
    bullets  – list of key contributions
    is_last  – suppresses the connecting line below the dot
    """
    bullets_li = "".join(f"<li>{b}</li>" for b in bullets)
    # line_html = "" if is_last else '<div class="tl-line"></div>'
    line_html = '<div class="tl-line last"></div>' if is_last else '<div class="tl-line"></div>'

    st.markdown(f"""
    <div class="tl-row">
        <div class="tl-dot-wrap">
            <div class="tl-dot"></div>
            {line_html}
        </div>
        <div class="tl-card">
            <p class="tl-company">{title}</p>
            <p class="tl-role">{subtitle}</p>
            <span class="tl-date">{date}</span>
            <ul class="tl-bullet">{bullets_li}</ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Grouped skill pills
# ---------------------------------------------------------------------------
def render_skills(grouped: dict[str, list[str]]):
    """
    grouped – {category_label: [skill, …]}
    Colour cycles through sp-indigo / sp-violet / sp-emerald / sp-rose / sp-amber
    """
    # colours = ["sp-indigo", "sp-violet", "sp-emerald", "sp-rose", "sp-amber"]
    colours = ["sp-indigo", "sp-emerald", "sp-violet", "sp-slate", "sp-slate"]
    html = ""
    for i, (category, skills) in enumerate(grouped.items()):
        cls = colours[i % len(colours)]
        pills = "".join(f'<span class="skill-pill {cls}">{s}</span>' for s in skills)
        html += f'<div class="skill-group-title">{category}</div><div class="skill-pills">{pills}</div>'
    st.markdown(f'<div class="glass-card">{html}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Award / certification row
# ---------------------------------------------------------------------------
def render_award(badge_emoji: str, badge_class: str, title: str, meta: str):
    st.markdown(f"""
    <div class="award-row">
        <div class="award-badge {badge_class}">{badge_emoji}</div>
        <div class="award-text">
            <h4>{title}</h4>
            <p>{meta}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# CTA banner
# ---------------------------------------------------------------------------
def render_cta():
    # st.markdown("""
    # <div class="cta-banner">
    #     <h2>💬 Want to explore further?</h2>
    #     <p>Use the AI-powered chatbot on the Top right to ask anything about experience, projects, skills, or background.</p>
    # </div>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <div class="cta-banner">
        <h2>💬 Want to explore further details?</h2>
        <p>Use the AI-powered chatbot on the 
                <span style="color:#ffffff; font-weight:bold;">
                    ⬆ top right side
                </span> 
            to ask anything about experience, projects, skills, or background.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Chat page header
# ---------------------------------------------------------------------------
def render_chat_header(name: str):
    # st.markdown(f"""
    # <div class="chat-header">
    #     <h2>🤖 AI Assistant</h2>
    #     <p>Ask me anything about <strong style="color:#a5b4fc;">{name}</strong> — experience, projects, skills, or background.</p>
    # </div>
    # """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="chat-header">
        <h2>🤖 AI Assistant</h2>
        <p>Hello 👋! I'm a digital twin of <strong style="color:#a5b4fc;">{name}</strong> — Ask me anything about my experience, projects, skills, or background.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Single chat bubble
# ---------------------------------------------------------------------------
def render_chat_bubble(role: str, content: str):
    """role: 'user' | 'assistant'"""
    side  = "user" if role == "user" else ""
    acls  = "user" if role == "user" else "bot"
    # icon  = "👤" if role == "user" else "🤖"
    icon  = "👤" if role == "user" else "🧠"
    # st.markdown(f"""
    # <div class="chat-bubble {side}">
    #     <div class="bubble-avatar {acls}">{icon}</div>
    #     <div class="bubble-text {acls}">{content}</div>
    # </div>
    # """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="chat-bubble {side}">
        <div >{icon}</div>
        <div class="bubble-text {acls}">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session state bootstrap
# ---------------------------------------------------------------------------
def initialize_session_state():
    for key, default in (
        ("chat_history", []),
        ("chatbot",      None),
        ("current_page", "Home"),
    ):
        if key not in st.session_state:
            st.session_state[key] = default