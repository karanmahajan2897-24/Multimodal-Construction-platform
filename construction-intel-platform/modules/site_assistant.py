"""
Tab 4 – Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Weather-based dynamic safety alerts + multi-turn construction engineering chatbot.
"""

import streamlit as st
from utils.demo_data import DEMO_WEATHER_ALERTS, DEMO_CHAT_RESPONSES
from utils.gemini_client import call_gemini_text

# ─── Constants ────────────────────────────────────────────────────────────────

WEATHER_OPTIONS = ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"]

CHAT_SYSTEM_PROMPT = """You are an expert construction engineering assistant with deep knowledge of:
- Indian Standards (IS codes): IS 456, IS 1786, IS 2950, IS 13920, IS 800, IS 875, IS 10262
- OSHA 29 CFR 1926 construction safety regulations
- Structural engineering (RCC, steel, masonry)
- Foundation design (isolated, raft, pile)
- Concrete mix design and quality control
- Construction project management and scheduling
- Cost estimation and Bill of Quantities
- Building materials: TMT steel, OPC/PPC cement, AAC blocks
- MEP (Mechanical, Electrical, Plumbing) coordination

Provide precise, practical, and actionable engineering guidance. When referencing standards, cite specific clause numbers. 
Be concise but thorough. Use bullet points and structured answers when helpful.
Always prioritize safety and code compliance in your recommendations.

User message: """

SUGGESTED_QUESTIONS = [
    "💧 What is the water-cement ratio for M30 concrete?",
    "🏗️ How do I design an isolated footing for a 3m × 3m column?",
    "⚙️ What is the minimum cover for RCC columns per IS 456?",
    "🔩 How many TMT bars are needed for a 230mm × 450mm beam?",
    "📏 What is the maximum slump for pump concrete?",
    "🧱 What are the steps for post-monsoon concrete repair?",
]


# ─── Weather alerts renderer ──────────────────────────────────────────────────

def _render_weather_alerts(condition: str):
    """Render weather-specific safety alerts."""

    data = DEMO_WEATHER_ALERTS.get(condition, DEMO_WEATHER_ALERTS["Normal"])
    alert_level = data.get("alert_level", "ALL CLEAR")
    color = data.get("color", "#10B981")
    icon = data.get("icon", "✅")
    headline = data.get("headline", "")
    alerts = data.get("alerts", [])

    # Alert banner
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color}18, {color}08);
            border: 2px solid {color}50;
            border-radius: 14px;
            padding: 1.25rem 1.75rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <div style="font-size: 2.5rem;">{icon}</div>
            <div>
                <div style="font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: {color}; margin-bottom: 0.2rem;">{alert_level}</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: var(--text-primary);">{headline}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Severity map for rendering
    sev_icons = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}

    for alert in alerts:
        sev = alert.get("severity", "Low")
        sev_icon = sev_icons.get(sev, "🟢")
        sev_css = {"Critical": "non-compliant", "High": "high", "Medium": "medium", "Low": "low"}.get(sev, "low")

        st.markdown(
            f"""
            <div class="weather-alert">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="weather-alert-title">{sev_icon} {alert.get('category','')}</div>
                    <span class="status-pill {sev_css}" style="font-size:0.65rem;">{sev}</span>
                </div>
                <div class="weather-alert-body">{alert.get('action','')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─── Chat engine ──────────────────────────────────────────────────────────────

def _get_demo_response(user_message: str) -> str:
    """Return a canned demo response when no API key is set."""
    msg_lower = user_message.lower()
    for keyword, response in DEMO_CHAT_RESPONSES.items():
        if keyword in msg_lower:
            return response
    return DEMO_CHAT_RESPONSES["default"]


def _chat_response(gemini_model, user_message: str, is_demo: bool, chat_history: list) -> str:
    """Get chat response from Gemini or demo fallback."""
    if is_demo:
        return _get_demo_response(user_message)

    # Build contextual prompt with recent history
    context = ""
    for msg in chat_history[-6:]:  # Last 3 pairs for context
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"

    full_prompt = CHAT_SYSTEM_PROMPT + user_message
    if context:
        full_prompt = f"Previous conversation:\n{context}\n\n{full_prompt}"

    return call_gemini_text(gemini_model, full_prompt)


# ─── Main render function ─────────────────────────────────────────────────────

def render_site_assistant_tab(gemini_model, is_demo: bool):
    """Render the Daily Site Assistant & Weather Advisory tab."""

    if is_demo:
        st.markdown(
            '<div class="demo-banner">🔬 <strong>Demo Mode</strong> — Weather alerts use reference data. '
            "Chatbot responses are pre-configured. Add Gemini API key for live AI chat.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="section-header">
            <div class="section-icon">🌤️</div>
            <div>
                <div class="section-title">Daily Site Assistant & Weather Advisory</div>
                <div class="section-sub">Real-time weather safety protocols · Multi-turn AI construction engineering assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Split layout: alerts left, chat right ────────
    col_weather, col_chat = st.columns([1, 1.2], gap="large")

    # ── WEATHER PANEL ─────────────────────────────────
    with col_weather:
        st.markdown("#### 🌡️ Current Site Weather Condition")

        selected_weather = st.selectbox(
            "Select weather condition",
            WEATHER_OPTIONS,
            key="weather_select",
            help="Select your site's current weather to view tailored safety protocols."
        )

        _render_weather_alerts(selected_weather)

        # Quick site status panel
        st.markdown(
            """
            <div class="section-header" style="margin-top:1rem;">
                <div class="section-icon">📋</div>
                <div><div class="section-title">Daily Checklist Status</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        checklist_items = [
            ("Toolbox Talk Conducted", "green"),
            ("PPE Gate Check Done", "green"),
            ("Equipment Pre-Op Inspection", "orange"),
            ("Concrete QC Slump Test", "orange"),
            ("Site Housekeeping Complete", "gray"),
        ]

        for item, status in checklist_items:
            icon = "✅" if status == "green" else ("⏳" if status == "orange" else "⬜")
            col_color = "#10B981" if status == "green" else ("#FBBF24" if status == "orange" else "#475569")
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:0.6rem; padding:0.4rem 0.6rem;
                     background:var(--bg-card); border-radius:6px; margin-bottom:0.3rem;">
                    <span style="font-size:0.9rem;">{icon}</span>
                    <span style="font-size:0.82rem; color:var(--text-muted);">{item}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── CHATBOT PANEL ─────────────────────────────────
    with col_chat:
        st.markdown("#### 🤖 Construction Engineering AI Assistant")

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [
                {
                    "role": "assistant",
                    "content": (
                        "👋 Hello! I'm your **AI Construction Engineering Assistant** — "
                        "powered by Google Gemini.\n\n"
                        "I can help you with:\n"
                        "• Mix design calculations (IS 10262)\n"
                        "• Structural member sizing (IS 456, IS 800)\n"
                        "• Foundation design (IS 2950)\n"
                        "• IS code compliance queries\n"
                        "• Site safety protocols\n\n"
                        "Ask me anything about your construction project! 🏗️"
                    )
                }
            ]

        # Render chat messages
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="👷"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(msg["content"])

        # Suggested questions (only if chat is fresh)
        if len(st.session_state["chat_history"]) <= 1:
            st.markdown(
                "<div style='font-size:0.78rem; color:var(--text-dim); margin-top:0.5rem; margin-bottom:0.4rem;'>💡 <strong>Suggested questions:</strong></div>",
                unsafe_allow_html=True,
            )
            for i, q in enumerate(SUGGESTED_QUESTIONS):
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    _send_chat(gemini_model, q.split(" ", 1)[1] if " " in q else q, is_demo)
                    st.rerun()

        # Chat input
        user_input = st.chat_input(
            "Ask about mix design, IS codes, structural analysis, safety...",
            key="chat_input"
        )

        if user_input:
            _send_chat(gemini_model, user_input, is_demo)
            st.rerun()

        # Clear chat button
        if len(st.session_state.get("chat_history", [])) > 1:
            if st.button("🗑️ Clear Chat History", key="clear_chat"):
                st.session_state["chat_history"] = [st.session_state["chat_history"][0]]
                st.rerun()


def _send_chat(gemini_model, user_message: str, is_demo: bool):
    """Append user message and get AI response."""
    st.session_state["chat_history"].append({"role": "user", "content": user_message})
    try:
        response = _chat_response(
            gemini_model,
            user_message,
            is_demo,
            st.session_state["chat_history"]
        )
    except Exception as e:
        response = f"⚠️ I encountered an error: {e}. Please check your API key and try again."
    st.session_state["chat_history"].append({"role": "assistant", "content": response})
