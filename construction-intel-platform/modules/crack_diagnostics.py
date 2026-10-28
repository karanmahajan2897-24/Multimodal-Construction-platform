"""
Tab 2 – Crack Diagnostics & Structural Integrity (Epic 2)
Multimodal Gemini analysis for concrete defect classification.
"""

import json
import streamlit as st
from utils.demo_data import DEMO_CRACK_ANALYSIS
from utils.gemini_client import call_gemini_vision, extract_json_from_response

# ─── Gemini prompt ────────────────────────────────────────────────────────────

CRACK_PROMPT = """
You are a licensed structural engineer and materials scientist specializing in concrete pathology and repair.

Analyze this image of a concrete or masonry surface and return a STRICT JSON object (no extra text, no markdown fences):

{
  "defect_type": "<one of: Hairline Crack | Settlement Crack | Structural Shear Crack | Thermal Expansion Crack | Spalling | Efflorescence | Delamination | Corrosion Stain | No Defect Detected>",
  "confidence": <integer 0-100>,
  "crack_width_mm": <float, estimated width in millimetres, null if not a crack>,
  "length_estimate_cm": <float, estimated visible length in cm, null if not applicable>,
  "depth_assessment": "<Superficial | Medium - penetrates plaster | Deep - structural concern | Unknown>",
  "location_description": "<where on the structure the defect appears and orientation>",
  "root_causes": [
    "<cause 1>",
    "<cause 2>"
  ],
  "structural_impact": "<plain-English assessment of structural implications>",
  "urgency": "<Immediate | High | Medium | Low | Monitor Only>",
  "recommended_repairs": [
    {
      "repair": "<repair method name>",
      "description": "<detailed method description with applicable IS/ACI standard>",
      "estimated_cost_inr": "<range as string>",
      "timeline": "<expected timeline>"
    }
  ],
  "applicable_standards": [
    "<IS/ACI/ASTM reference>"
  ]
}

Be specific. Estimate crack width based on visual proportions and context. If the image does not show a structural defect, set defect_type to 'No Defect Detected'.
"""


# ─── Helper functions ─────────────────────────────────────────────────────────

def _urgency_color(urgency: str) -> str:
    return {
        "Immediate": "#EF4444",
        "High": "#F97316",
        "Medium": "#FBBF24",
        "Low": "#10B981",
        "Monitor Only": "#38BDF8",
    }.get(urgency, "#FBBF24")


def _urgency_pill(urgency: str) -> str:
    return {
        "Immediate": "non-compliant",
        "High": "high",
        "Medium": "medium",
        "Low": "low",
        "Monitor Only": "low",
    }.get(urgency, "medium")


def _confidence_bar(confidence: int) -> str:
    color = "#10B981" if confidence >= 75 else "#FBBF24" if confidence >= 50 else "#EF4444"
    return f"""
    <div style="margin-top:0.4rem;">
        <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:var(--text-dim); margin-bottom:3px;">
            <span>AI Confidence</span><span>{confidence}%</span>
        </div>
        <div style="background:var(--border); border-radius:4px; height:6px; overflow:hidden;">
            <div style="width:{confidence}%; height:100%; background:{color}; border-radius:4px; transition:width 0.5s;"></div>
        </div>
    </div>
    """


def _defect_icon(defect_type: str) -> str:
    icons = {
        "Hairline Crack": "🔍",
        "Settlement Crack": "📐",
        "Structural Shear Crack": "⚠️",
        "Thermal Expansion Crack": "🌡️",
        "Spalling": "💥",
        "Efflorescence": "💧",
        "Delamination": "📋",
        "Corrosion Stain": "🔴",
        "No Defect Detected": "✅",
    }
    return icons.get(defect_type, "🔎")


# ─── Main render function ─────────────────────────────────────────────────────

def render_crack_tab(gemini_model, is_demo: bool):
    """Render the Crack Diagnostics & Structural Integrity tab."""

    if is_demo:
        st.markdown(
            '<div class="demo-banner">🔬 <strong>Demo Mode</strong> — Showing sample crack analysis. '
            "Add your Gemini API key to analyze real structural photos.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="section-header">
            <div class="section-icon">🏗️</div>
            <div>
                <div class="section-title">Crack Diagnostics & Structural Integrity</div>
                <div class="section-sub">IS 456:2000 · IS 13935:2009 · ACI 224R-01 · Concrete Pathology Analysis</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_up, col_ref = st.columns([1, 1], gap="medium")

    with col_up:
        uploaded = st.file_uploader(
            "Upload concrete / wall surface image",
            type=["jpg", "jpeg", "png", "webp"],
            key="crack_uploader",
            help="Upload a photo of a cracked or potentially damaged concrete surface.",
        )
        if uploaded:
            st.image(uploaded, caption="Surface Under Analysis", use_container_width=True)

    with col_ref:
        st.markdown(
            """
            <div class="info-card">
                <div class="card-title">🔎 Detectable Defect Types</div>
                <div class="card-body" style="display:grid; grid-template-columns:1fr 1fr; gap:0.4rem; margin-top:0.4rem;">
                    <div>🔍 Hairline Crack</div>
                    <div>📐 Settlement Crack</div>
                    <div>⚠️ Structural Shear</div>
                    <div>🌡️ Thermal Expansion</div>
                    <div>💥 Spalling</div>
                    <div>💧 Efflorescence</div>
                    <div>📋 Delamination</div>
                    <div>🔴 Corrosion Stain</div>
                </div>
            </div>
            <div class="info-card" style="margin-top:0.75rem;">
                <div class="card-title">📏 Measurement Reference</div>
                <div class="card-body">
                    <b>Crack Width Classification (IS 456:2000):</b><br/>
                    • &lt;0.3 mm → Hairline (aesthetic concern)<br/>
                    • 0.3–1.0 mm → Fine (monitor)<br/>
                    • 1.0–3.0 mm → Medium (repair required)<br/>
                    • &gt;3.0 mm → Wide (structural assessment)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍 Run Crack Diagnostics", key="analyze_crack", use_container_width=True)

    if analyze_btn or (is_demo and "crack_result" not in st.session_state):
        with st.spinner("🤖 Structural AI analyzing defect patterns..."):
            try:
                if is_demo or not uploaded:
                    result = DEMO_CRACK_ANALYSIS
                else:
                    image_bytes = uploaded.read()
                    mime = "image/png" if uploaded.name.lower().endswith(".png") else "image/jpeg"
                    raw = call_gemini_vision(gemini_model, CRACK_PROMPT, image_bytes, mime)
                    result = extract_json_from_response(raw)
                    if not result:
                        st.error("⚠️ Could not parse AI response. Please try again.")
                        return
                st.session_state["crack_result"] = result
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                return

    if "crack_result" in st.session_state:
        _render_crack_results(st.session_state["crack_result"])


def _render_crack_results(result: dict):
    """Render crack analysis results."""

    defect_type = result.get("defect_type", "Unknown")
    confidence = result.get("confidence", 0)
    crack_width = result.get("crack_width_mm")
    urgency = result.get("urgency", "Medium")
    structural_impact = result.get("structural_impact", "")
    root_causes = result.get("root_causes", [])
    repairs = result.get("recommended_repairs", [])
    standards = result.get("applicable_standards", [])
    depth = result.get("depth_assessment", "Unknown")
    location = result.get("location_description", "")

    st.markdown("<br/>", unsafe_allow_html=True)
    urgency_color = _urgency_color(urgency)
    defect_icon = _defect_icon(defect_type)

    # ── Main defect card ─────────────────────────────
    st.markdown(
        f"""
        <div class="score-ring-wrap" style="gap:2rem;">
            <div style="text-align:center; flex-shrink:0;">
                <div style="font-size:3.5rem; margin-bottom:0.25rem;">{defect_icon}</div>
                {_confidence_bar(confidence)}
            </div>
            <div class="score-info" style="flex:1;">
                <h3 style="font-size:1.3rem; color:#F1F5F9;">{defect_type}</h3>
                <p style="margin:0.25rem 0;">{location}</p>
                <div style="margin-top:0.6rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
                    <span class="status-pill {_urgency_pill(urgency)}">🚨 {urgency} Urgency</span>
                    <span class="status-pill partial">📏 Depth: {depth}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Metric cards ─────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (col1, "CRACK WIDTH", f"{crack_width}" if crack_width else "N/A", "millimetres", "danger" if crack_width and crack_width > 3 else "warning"),
        (col2, "LENGTH ESTIMATE", f"{result.get('length_estimate_cm','—')}", "centimetres", "primary"),
        (col3, "CONFIDENCE", f"{confidence}%", "AI accuracy", "success" if confidence >= 75 else "warning"),
        (col4, "URGENCY", urgency, "", _urgency_pill(urgency) if urgency in ["Immediate","High"] else "success"),
    ]
    for col, label, value, sub, cls in metrics:
        with col:
            st.markdown(
                f"""
                <div class="metric-card {cls}">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value {cls}" style="font-size:1.4rem; word-break:break-word;">{value}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br/>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        # ── Structural Impact ─────────────────────────
        st.markdown(
            f"""
            <div class="section-header">
                <div class="section-icon">🏛️</div>
                <div><div class="section-title">Structural Impact Assessment</div></div>
            </div>
            <div class="info-card">
                <div class="card-body">{structural_impact}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Root Causes ───────────────────────────────
        st.markdown(
            """
            <div class="section-header" style="margin-top:1.25rem;">
                <div class="section-icon">🔍</div>
                <div><div class="section-title">Root Cause Analysis</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        causes_html = "".join(
            f'<div style="padding:0.5rem 0.75rem; background:var(--bg-card2); border-radius:6px; margin-bottom:0.4rem; font-size:0.85rem; color:var(--text-muted);">🔸 {c}</div>'
            for c in root_causes
        )
        st.markdown(causes_html, unsafe_allow_html=True)

        # ── Standards ─────────────────────────────────
        if standards:
            st.markdown(
                """
                <div class="section-header" style="margin-top:1.25rem;">
                    <div class="section-icon">📜</div>
                    <div><div class="section-title">Applicable Standards</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            std_html = "".join(
                f'<span class="status-pill low" style="margin:0.2rem; display:inline-flex;">{s}</span>'
                for s in standards
            )
            st.markdown(f"<div style='line-height:2.2;'>{std_html}</div>", unsafe_allow_html=True)

    with col_right:
        # ── Recommended Repairs ───────────────────────
        st.markdown(
            """
            <div class="section-header">
                <div class="section-icon">🔧</div>
                <div><div class="section-title">Recommended Engineering Repairs</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for i, repair in enumerate(repairs):
            st.markdown(
                f"""
                <div class="info-card" style="margin-bottom:0.75rem; border-left:4px solid var(--primary);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <div class="card-title" style="margin:0;">🔧 {repair.get('repair','')}</div>
                        <span class="status-pill low" style="flex-shrink:0; margin-left:0.5rem;">{repair.get('timeline','')}</span>
                    </div>
                    <div class="card-body">{repair.get('description','')}</div>
                    <div class="card-meta" style="margin-top:0.4rem;">
                        💰 Estimated Cost: <strong>{repair.get('estimated_cost_inr','—')}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Download ─────────────────────────────────────
    st.markdown("<br/>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Crack Diagnostics Report (JSON)",
        data=json.dumps(result, indent=2),
        file_name="crack_diagnostics_report.json",
        mime="application/json",
        use_container_width=True,
    )
