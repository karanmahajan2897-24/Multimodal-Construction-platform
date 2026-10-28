"""
Tab 1 – Site Safety & PPE Audit (Epic 2)
Multimodal Gemini analysis of construction site photos for PPE compliance.
"""

import json
import streamlit as st
from utils.demo_data import DEMO_SAFETY_AUDIT
from utils.gemini_client import call_gemini_vision, extract_json_from_response

# ─── Gemini prompt ────────────────────────────────────────────────────────────

SAFETY_PROMPT = """
You are a certified construction site safety inspector with expertise in OSHA 29 CFR 1926 (US) and Indian Standard IS 456:2000 / NBC 2016 standards.

Analyze this construction site photograph and return a STRICT JSON object with the following schema (no extra text, no markdown fences):

{
  "safety_score": <integer 0-100>,
  "overall_status": "<one of: COMPLIANT | NEEDS IMPROVEMENT | NON-COMPLIANT | CRITICAL>",
  "analysis_summary": "<2-3 sentence plain-English summary of site safety status>",
  "ppe_detection": {
    "helmets": {
      "status": "<COMPLIANT | PARTIAL | NON-COMPLIANT | NOT_APPLICABLE>",
      "compliant_count": <integer or null>,
      "total_workers": <integer or null>,
      "notes": "<brief note>"
    },
    "high_vis_vests": {
      "status": "<COMPLIANT | PARTIAL | NON-COMPLIANT | NOT_APPLICABLE>",
      "compliant_count": <integer or null>,
      "total_workers": <integer or null>,
      "notes": "<brief note>"
    },
    "steel_toe_boots": {
      "status": "<COMPLIANT | PARTIAL | NON-COMPLIANT | NOT_APPLICABLE>",
      "compliant_count": <integer or null>,
      "total_workers": <integer or null>,
      "notes": "<brief note>"
    },
    "safety_harnesses": {
      "status": "<COMPLIANT | PARTIAL | NON-COMPLIANT | NOT_APPLICABLE>",
      "compliant_count": <integer or null>,
      "total_workers": <integer or null>,
      "notes": "<brief note>"
    }
  },
  "site_hazards": [
    {
      "hazard": "<description>",
      "severity": "<Critical | High | Medium | Low>",
      "osha_standard": "<relevant OSHA clause or N/A>",
      "is_standard": "<relevant IS clause or N/A>",
      "remedy": "<specific corrective action>"
    }
  ]
}

Be precise and specific. If workers are not clearly visible, note that in the hazard list.
"""


# ─── PPE status helpers ───────────────────────────────────────────────────────

def _ppe_pill_class(status: str) -> str:
    mapping = {
        "COMPLIANT": "compliant",
        "PARTIAL": "partial",
        "NON-COMPLIANT": "non-compliant",
        "NOT_APPLICABLE": "low",
    }
    return mapping.get(status.upper(), "partial")


def _ppe_icon(status: str) -> str:
    mapping = {
        "COMPLIANT": "✅",
        "PARTIAL": "⚠️",
        "NON-COMPLIANT": "❌",
        "NOT_APPLICABLE": "➖",
    }
    return mapping.get(status.upper(), "⚠️")


def _severity_class(severity: str) -> str:
    return {
        "Critical": "hazard-critical",
        "High": "hazard-high",
        "Medium": "hazard-medium",
        "Low": "hazard-low",
    }.get(severity, "hazard-medium")


def _severity_pill(severity: str) -> str:
    return severity.lower()


def _score_color(score: int) -> str:
    if score >= 80:
        return "#10B981"
    elif score >= 60:
        return "#FBBF24"
    elif score >= 40:
        return "#F97316"
    return "#EF4444"


# ─── Main render function ─────────────────────────────────────────────────────

def render_safety_tab(gemini_model, is_demo: bool):
    """Render the Site Safety & PPE Audit tab."""

    # Demo banner
    if is_demo:
        st.markdown(
            '<div class="demo-banner">🔬 <strong>Demo Mode</strong> — Showing sample analysis. '
            "Add your Gemini API key in the sidebar to analyze real site photos.</div>",
            unsafe_allow_html=True,
        )

    # Header
    st.markdown(
        """
        <div class="section-header">
            <div class="section-icon">🦺</div>
            <div>
                <div class="section-title">Site Safety & PPE Audit</div>
                <div class="section-sub">OSHA 29 CFR 1926 · IS 456:2000 · NBC 2016 Compliance Analysis</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # File uploader
    uploaded = st.file_uploader(
        "Upload construction site photo for PPE analysis",
        type=["jpg", "jpeg", "png", "webp"],
        key="safety_uploader",
        help="Upload JPG or PNG photo of your construction site. Supports multiple workers.",
    )

    col_img, col_info = st.columns([1, 1], gap="medium")

    with col_img:
        if uploaded:
            st.image(uploaded, caption="Uploaded Site Photo", use_container_width=True)
        else:
            st.markdown(
                """
                <div class="info-card" style="text-align:center; padding: 3rem 1rem;">
                    <div style="font-size:3rem;">📸</div>
                    <div style="color:var(--text-muted); margin-top:0.5rem; font-size:0.85rem;">
                        Upload a site photo to begin AI analysis
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            """
            <div class="info-card">
                <div class="card-title">📋 Analysis Coverage</div>
                <div class="card-body">
                    <b>PPE Detection</b><br/>
                    • Hard hats / Helmets (IS 2925)<br/>
                    • High-visibility vests (IS 15809)<br/>
                    • Steel-toe boots (IS 15298)<br/>
                    • Safety harnesses (IS 3521)<br/><br/>
                    <b>Hazard Identification</b><br/>
                    • Fall protection compliance<br/>
                    • Electrical safety zones<br/>
                    • Excavation & scaffolding risks<br/>
                    • Chemical / dust exposure
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    analyze_btn = st.button("🔍 Analyze Site Safety", key="analyze_safety", use_container_width=True)

    if analyze_btn or (is_demo and "safety_result" not in st.session_state):
        with st.spinner("🤖 AI Safety Inspector analyzing site conditions..."):
            try:
                if is_demo or not uploaded:
                    result = DEMO_SAFETY_AUDIT
                else:
                    image_bytes = uploaded.read()
                    mime = "image/png" if uploaded.name.lower().endswith(".png") else "image/jpeg"
                    raw = call_gemini_vision(gemini_model, SAFETY_PROMPT, image_bytes, mime)
                    result = extract_json_from_response(raw)
                    if not result:
                        st.error("⚠️ Could not parse AI response. Please try again.")
                        return
                st.session_state["safety_result"] = result
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                return

    if "safety_result" in st.session_state:
        _render_safety_results(st.session_state["safety_result"])


def _render_safety_results(result: dict):
    """Render the structured safety analysis results."""

    score = result.get("safety_score", 0)
    status = result.get("overall_status", "UNKNOWN")
    summary = result.get("analysis_summary", "")
    ppe = result.get("ppe_detection", {})
    hazards = result.get("site_hazards", [])
    score_color = _score_color(score)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Score ring + summary ─────────────────────────
    st.markdown(
        f"""
        <div class="score-ring-wrap">
            <div class="score-circle" style="background: conic-gradient({score_color} 0% {score}%, #1E293B {score}% 100%); box-shadow: 0 0 30px {score_color}33;">
                <div class="score-number" style="color:{score_color};">{score}</div>
                <div class="score-label">/ 100</div>
            </div>
            <div class="score-info">
                <h3>Safety Score</h3>
                <p>{summary}</p>
                <div style="margin-top:0.6rem;">
                    <span class="status-pill {_severity_pill(status.replace(' ','_').lower()) if status not in ['COMPLIANT','NEEDS IMPROVEMENT','NON-COMPLIANT','CRITICAL'] else ('compliant' if status=='COMPLIANT' else ('partial' if status=='NEEDS IMPROVEMENT' else 'non-compliant'))}">
                        {status}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Metric cards row ─────────────────────────────
    hazard_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for h in hazards:
        sev = h.get("severity", "Low")
        hazard_counts[sev] = hazard_counts.get(sev, 0) + 1

    col1, col2, col3, col4 = st.columns(4)
    metric_data = [
        (col1, "SAFETY SCORE", f"{score}", "/100", "primary" if score >= 60 else "danger"),
        (col2, "CRITICAL HAZARDS", str(hazard_counts["Critical"]), "identified", "danger" if hazard_counts["Critical"] > 0 else "success"),
        (col3, "HIGH HAZARDS", str(hazard_counts["High"]), "identified", "warning" if hazard_counts["High"] > 0 else "success"),
        (col4, "TOTAL HAZARDS", str(len(hazards)), "site risks", "primary"),
    ]
    for col, label, value, sub, cls in metric_data:
        with col:
            st.markdown(
                f"""
                <div class="metric-card {cls}">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value {cls}">{value}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── PPE Checklist ────────────────────────────────
    st.markdown(
        """
        <div class="section-header" style="margin-top:1.5rem;">
            <div class="section-icon">🦺</div>
            <div>
                <div class="section-title">PPE Compliance Checklist</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ppe_items = [
        ("🪖", "Hard Hats / Helmets", "helmets"),
        ("🦺", "High-Visibility Vests", "high_vis_vests"),
        ("👢", "Steel-Toe Boots", "steel_toe_boots"),
        ("🔗", "Safety Harnesses", "safety_harnesses"),
    ]

    for icon, label, key in ppe_items:
        item = ppe.get(key, {})
        item_status = item.get("status", "NOT_APPLICABLE")
        pill_cls = _ppe_pill_class(item_status)
        pill_icon = _ppe_icon(item_status)
        count_str = ""
        if item.get("compliant_count") is not None and item.get("total_workers"):
            count_str = f"  ({item['compliant_count']}/{item['total_workers']} workers)"
        notes = item.get("notes", "")

        st.markdown(
            f"""
            <div class="ppe-item">
                <div>
                    <div class="ppe-name">{icon} {label}{count_str}</div>
                    <div class="ppe-note">{notes}</div>
                </div>
                <span class="status-pill {pill_cls}">{pill_icon} {item_status.replace('_', ' ')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Site Hazards ─────────────────────────────────
    if hazards:
        st.markdown(
            """
            <div class="section-header" style="margin-top:1.5rem;">
                <div class="section-icon">⚠️</div>
                <div>
                    <div class="section-title">Identified Site Hazards & Corrective Remedies</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i, hazard in enumerate(hazards):
            sev = hazard.get("severity", "Medium")
            card_cls = _severity_class(sev)
            pill_cls = _severity_pill(sev)
            st.markdown(
                f"""
                <div class="info-card {card_cls}">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                        <div class="card-title">#{i+1} — {hazard.get('hazard','')}</div>
                        <span class="status-pill {pill_cls}" style="flex-shrink:0; margin-left:1rem;">{sev}</span>
                    </div>
                    <div class="card-body">
                        <strong>🔧 Corrective Remedy:</strong> {hazard.get('remedy','N/A')}
                    </div>
                    <div class="card-meta" style="margin-top:0.5rem;">
                        OSHA: {hazard.get('osha_standard','N/A')} &nbsp;|&nbsp; IS: {hazard.get('is_standard','N/A')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Downloadable JSON ────────────────────────────
    st.markdown("<br/>", unsafe_allow_html=True)
    json_str = json.dumps(result, indent=2)
    st.download_button(
        label="📥 Download Full Safety Report (JSON)",
        data=json_str,
        file_name="site_safety_audit_report.json",
        mime="application/json",
        use_container_width=True,
    )
