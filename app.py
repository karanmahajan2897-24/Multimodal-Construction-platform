"""
╔══════════════════════════════════════════════════════════════════╗
║   Multimodal Construction Intelligence Platform                  ║
║   Skill Wallet Capstone Project 1                                ║
║   Built with: Streamlit · Google Gemini · Pollinations AI        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from utils.styling import inject_custom_css
from utils.gemini_client import init_gemini
from modules.safety_audit import render_safety_tab
from modules.crack_diagnostics import render_crack_tab
from modules.valuation import render_valuation_tab
from modules.site_assistant import render_site_assistant_tab

# ─── Page configuration ───────────────────────────────────────────────────────

st.set_page_config(
    page_title="Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "About": "Multimodal Construction Intelligence Platform — Skill Wallet Capstone Project 1",
    },
)

# ─── Inject CSS ───────────────────────────────────────────────────────────────

st.markdown(inject_custom_css(), unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    # Brand
    st.markdown(
        """
        <div style="text-align:center; padding: 0.5rem 0 1.25rem;">
            <div style="font-size:2.5rem;">🏗️</div>
            <div style="font-weight:800; font-size:1rem; color:#F1F5F9; margin-top:0.3rem; line-height:1.3;">
                Construction<br/>Intelligence Platform
            </div>
            <div style="font-size:0.65rem; color:#64748B; margin-top:0.2rem; letter-spacing:1px; text-transform:uppercase;">
                Skill Wallet Capstone · Project 1
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── API Key input ─────────────────────────────────
    st.markdown('<div class="sidebar-title">🔑 Google Gemini API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "API Key",
        type="password",
        key="gemini_api_key",
        placeholder="AIza...",
        label_visibility="collapsed",
        help="Obtain your free API key at https://aistudio.google.com/app/apikey"
    )

    if api_key:
        try:
            gemini_model = init_gemini(api_key)
            is_demo = False
            st.markdown(
                '<div style="color:#10B981; font-size:0.78rem; margin-top:0.3rem;">✅ API key active — AI analysis enabled</div>',
                unsafe_allow_html=True,
            )
        except Exception as e:
            gemini_model = None
            is_demo = True
            st.markdown(
                f'<div style="color:#EF4444; font-size:0.78rem; margin-top:0.3rem;">❌ Invalid key: {str(e)[:60]}</div>',
                unsafe_allow_html=True,
            )
    else:
        gemini_model = None
        is_demo = True
        st.markdown(
            '<div style="color:#64748B; font-size:0.75rem; margin-top:0.3rem;">ℹ️ No key — running in <strong>Demo Mode</strong></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="font-size:0.7rem; color:#475569; margin-top:0.4rem;">'
        '🔗 <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#38BDF8;">Get free API key →</a>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Architecture Overview ─────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1.5rem;">🏛️ Architecture Overview</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size:0.78rem; color:#94A3B8; line-height:1.7;">
            <div style="padding:0.35rem 0.6rem; background:#1E293B; border-radius:6px; margin-bottom:0.35rem; border-left:3px solid #F97316;">
                🤖 <strong>Google Gemini 1.5 Flash</strong><br/>
                <span style="color:#64748B; font-size:0.7rem;">Vision + Text multimodal LLM</span>
            </div>
            <div style="padding:0.35rem 0.6rem; background:#1E293B; border-radius:6px; margin-bottom:0.35rem; border-left:3px solid #38BDF8;">
                🎨 <strong>Pollinations AI</strong><br/>
                <span style="color:#64748B; font-size:0.7rem;">Free architectural renders</span>
            </div>
            <div style="padding:0.35rem 0.6rem; background:#1E293B; border-radius:6px; margin-bottom:0.35rem; border-left:3px solid #10B981;">
                🐍 <strong>Streamlit</strong><br/>
                <span style="color:#64748B; font-size:0.7rem;">Python web app framework</span>
            </div>
            <div style="padding:0.35rem 0.6rem; background:#1E293B; border-radius:6px; border-left:3px solid #8B5CF6;">
                📊 <strong>Zero DB deps</strong><br/>
                <span style="color:#64748B; font-size:0.7rem;">Session state only · 1-click deploy</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Feature Navigation ────────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1.5rem;">🗺️ Module Navigation</div>', unsafe_allow_html=True)
    nav_items = [
        ("🦺", "Tab 1", "Site Safety & PPE Audit", "Epic 2"),
        ("🏗️", "Tab 2", "Crack Diagnostics", "Epic 2"),
        ("📊", "Tab 3", "Planning & Valuation", "Epic 3"),
        ("🌤️", "Tab 4", "Site Assistant & Weather", "Epic 5"),
    ]
    for icon, tab, name, epic in nav_items:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:0.6rem; padding:0.4rem 0.6rem;
                 background:#1E293B; border-radius:6px; margin-bottom:0.3rem;">
                <span>{icon}</span>
                <div>
                    <div style="font-size:0.78rem; font-weight:600; color:#F1F5F9;">{tab}: {name}</div>
                    <div style="font-size:0.65rem; color:#475569;">{epic}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Footer ────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-top:2rem; padding-top:1rem; border-top:1px solid #1E293B;
             text-align:center; font-size:0.65rem; color:#334155; line-height:1.6;">
            Skill Wallet Capstone Project 1<br/>
            Multimodal AI · IS 456 · OSHA · NBC 2016<br/>
            <span style="color:#1E293B;">────────────────</span><br/>
            Built with Streamlit + Google Gemini
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Main App Header ──────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div class="app-header">
        <div class="app-title">🏗️ Multimodal Construction Intelligence Platform</div>
        <div class="app-subtitle">
            AI-powered site safety · Structural diagnostics · Real estate valuation · Engineering assistant
        </div>
        <div class="app-badges">
            <span class="badge">Google Gemini 1.5 Flash</span>
            <span class="badge blue">IS 456:2000</span>
            <span class="badge blue">OSHA 29 CFR 1926</span>
            <span class="badge green">{'🟢 AI Enabled' if not is_demo else '🔵 Demo Mode'}</span>
            <span class="badge">NBC 2016</span>
            <span class="badge blue">Pollinations AI</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🏗️ Crack Diagnostics",
    "📊 Planning & Valuation",
    "🌤️ Site Assistant",
])

with tab1:
    render_safety_tab(gemini_model, is_demo)

with tab2:
    render_crack_tab(gemini_model, is_demo)

with tab3:
    render_valuation_tab()

with tab4:
    render_site_assistant_tab(gemini_model, is_demo)
