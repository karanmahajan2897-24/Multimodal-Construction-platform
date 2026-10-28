"""
Tab 3 – Planning & Real Estate Valuation (Epic 3)
Construction budget estimator, asset valuation, material metrics, and 3D render via Pollinations AI.
"""

import math
import requests
import streamlit as st

# ─── Constants ────────────────────────────────────────────────────────────────

# Base construction cost per sqft (INR) by structure type
BASE_COST_PER_SQFT = {
    "Residential Apartment (RCC Framed)": 2200,
    "Independent Villa / Bungalow": 2600,
    "Commercial Office Building": 3000,
    "Industrial Warehouse / Factory": 1800,
    "Mixed-Use Development": 2800,
    "High-Rise Residential (15+ floors)": 3400,
}

# Location tier multipliers
TIER_MULTIPLIERS = {
    "Tier 1 (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad)": 1.35,
    "Tier 2 (Pune, Ahmedabad, Kolkata, Jaipur, Surat)": 1.10,
    "Tier 3 (Smaller cities & semi-urban)": 0.90,
}

# Completion-stage capital deployment curve (% of total budget spent at % completion)
STAGE_SPEND = {
    0: 0.0, 10: 0.08, 20: 0.18, 30: 0.30, 40: 0.42,
    50: 0.55, 60: 0.67, 70: 0.78, 80: 0.88, 90: 0.95, 100: 1.0,
}

# Market valuation premium over construction cost by tier
MARKET_PREMIUM = {
    "Tier 1 (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad)": 1.85,
    "Tier 2 (Pune, Ahmedabad, Kolkata, Jaipur, Surat)": 1.45,
    "Tier 3 (Smaller cities & semi-urban)": 1.15,
}

# Steel requirement (kg per sqft) by structure type
STEEL_KG_PER_SQFT = {
    "Residential Apartment (RCC Framed)": 3.8,
    "Independent Villa / Bungalow": 3.2,
    "Commercial Office Building": 4.5,
    "Industrial Warehouse / Factory": 5.5,
    "Mixed-Use Development": 4.2,
    "High-Rise Residential (15+ floors)": 6.0,
}

# Cement requirement (bags of 50kg per sqft)
CEMENT_BAGS_PER_SQFT = {
    "Residential Apartment (RCC Framed)": 0.42,
    "Independent Villa / Bungalow": 0.38,
    "Commercial Office Building": 0.52,
    "Industrial Warehouse / Factory": 0.35,
    "Mixed-Use Development": 0.48,
    "High-Rise Residential (15+ floors)": 0.60,
}

MILESTONE_STAGES = [
    (10, "📋 Foundation Design & Approvals"),
    (20, "🏗️ Substructure / Foundation Work"),
    (35, "🧱 Superstructure – Ground Floor"),
    (55, "🏢 Superstructure – Upper Floors"),
    (70, "🪟 Brick Infill, Plastering & MEP Rough-In"),
    (85, "🎨 Finishing, Flooring & Façade"),
    (95, "⚡ MEP Completion & Testing"),
    (100, "🏆 Handover & Occupancy Certificate"),
]

# ─── Helper functions ─────────────────────────────────────────────────────────

def _inr_format(amount_inr: float) -> str:
    """Format INR amount into Lakhs or Crores."""
    if amount_inr >= 1e7:
        crores = amount_inr / 1e7
        return f"₹{crores:.2f} Cr"
    else:
        lakhs = amount_inr / 1e5
        return f"₹{lakhs:.2f} L"


def _interpolate_spend(completion: int) -> float:
    """Interpolate capital deployment curve for any completion %."""
    lower = (completion // 10) * 10
    upper = min(lower + 10, 100)
    if lower == upper:
        return STAGE_SPEND[lower]
    frac = (completion - lower) / 10
    return STAGE_SPEND[lower] + frac * (STAGE_SPEND[upper] - STAGE_SPEND[lower])


def _get_pollinations_image_url(prompt: str, width: int = 768, height: int = 512, seed: int = 42) -> str:
    """Generate Pollinations AI image URL for architectural rendering."""
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true&enhance=true"


# ─── Main render function ─────────────────────────────────────────────────────

def render_valuation_tab():
    """Render the Planning & Real Estate Valuation tab."""

    st.markdown(
        """
        <div class="section-header">
            <div class="section-icon">📊</div>
            <div>
                <div class="section-title">Planning & Real Estate Valuation Engine</div>
                <div class="section-sub">Budget Estimation · Market Valuation · Material Planning · Milestone Tracking</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Inputs ───────────────────────────────────────
    st.markdown("#### 🏗️ Project Configuration")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        structure_type = st.selectbox(
            "Structure Type",
            list(BASE_COST_PER_SQFT.keys()),
            key="val_structure",
            help="Select the primary structural category of your project."
        )
        location_tier = st.selectbox(
            "Location Tier",
            list(TIER_MULTIPLIERS.keys()),
            key="val_tier",
            help="Indian city tier affects land premium and labour costs."
        )
        project_name = st.text_input(
            "Project Name (optional)",
            value="",
            key="val_name",
            placeholder="e.g. Sky Vista Tower, Phase 2"
        )

    with col2:
        builtup_sqft = st.number_input(
            "Built-up Area (sqft)",
            min_value=500,
            max_value=500_000,
            value=2500,
            step=100,
            key="val_sqft",
            help="Total built-up / carpet area in square feet."
        )
        floors = st.number_input(
            "Number of Floors",
            min_value=1,
            max_value=60,
            value=3,
            step=1,
            key="val_floors"
        )
        completion_pct = st.slider(
            "Completion Percentage (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=5,
            key="val_completion",
            help="Current project completion percentage."
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Calculations ──────────────────────────────────
    base_rate = BASE_COST_PER_SQFT[structure_type]
    tier_mult = TIER_MULTIPLIERS[location_tier]
    market_mult = MARKET_PREMIUM[location_tier]

    total_budget_inr = builtup_sqft * base_rate * tier_mult * floors
    capex_fraction = _interpolate_spend(completion_pct)
    capex_incurred = total_budget_inr * capex_fraction
    market_valuation = total_budget_inr * market_mult * (completion_pct / 100) if completion_pct > 0 else 0

    steel_required_kg = builtup_sqft * floors * STEEL_KG_PER_SQFT[structure_type]
    steel_used_kg = steel_required_kg * capex_fraction
    cement_bags_total = builtup_sqft * floors * CEMENT_BAGS_PER_SQFT[structure_type]
    cement_bags_used = cement_bags_total * capex_fraction

    # ── Main valuation metrics ────────────────────────
    st.markdown(
        """
        <div class="section-header">
            <div class="section-icon">💰</div>
            <div><div class="section-title">Financial Valuation Summary</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            f"""
            <div class="val-card">
                <div class="val-currency">Total Project Budget</div>
                <div class="val-amount">{_inr_format(total_budget_inr)}</div>
                <div class="val-label">@ ₹{base_rate * tier_mult:,.0f}/sqft effective rate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""
            <div class="val-card">
                <div class="val-currency">CapEx Incurred</div>
                <div class="val-amount" style="font-size:1.4rem;">{_inr_format(capex_incurred)}</div>
                <div class="val-label">at {completion_pct}% completion ({capex_fraction*100:.0f}% deployed)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            f"""
            <div class="val-card">
                <div class="val-currency">Current Market Valuation</div>
                <div class="val-amount" style="font-size:1.4rem;">{_inr_format(market_valuation)}</div>
                <div class="val-label">{location_tier.split('(')[0].strip()} premium applied</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        # ── Material Requirements ─────────────────────
        st.markdown(
            """
            <div class="section-header">
                <div class="section-icon">🏗️</div>
                <div><div class="section-title">Material Quantity Metrics</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Steel
        st.markdown(
            f"""
            <div class="info-card">
                <div class="card-title">⚙️ Steel (TMT Fe500D)</div>
                <div style="display:flex; justify-content:space-between; margin-top:0.5rem;">
                    <div>
                        <div class="metric-value" style="font-size:1.5rem; color:var(--accent);">{steel_used_kg:,.0f} kg</div>
                        <div class="metric-sub">Used / Procured so far</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="metric-value" style="font-size:1.5rem; color:var(--text-muted);">{steel_required_kg:,.0f} kg</div>
                        <div class="metric-sub">Total Project Requirement</div>
                    </div>
                </div>
                <div style="margin-top:0.75rem; background:var(--border); border-radius:4px; height:8px; overflow:hidden;">
                    <div style="width:{capex_fraction*100:.0f}%; height:100%; background:linear-gradient(90deg, var(--accent), #0EA5E9); border-radius:4px;"></div>
                </div>
                <div class="card-meta" style="margin-top:0.3rem;">{capex_fraction*100:.0f}% procured · Remaining: {steel_required_kg - steel_used_kg:,.0f} kg</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Cement
        st.markdown(
            f"""
            <div class="info-card" style="margin-top:0.75rem;">
                <div class="card-title">🪨 Cement (OPC 53 Grade, 50kg bags)</div>
                <div style="display:flex; justify-content:space-between; margin-top:0.5rem;">
                    <div>
                        <div class="metric-value" style="font-size:1.5rem; color:var(--primary);">{cement_bags_used:,.0f}</div>
                        <div class="metric-sub">Bags used so far</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="metric-value" style="font-size:1.5rem; color:var(--text-muted);">{cement_bags_total:,.0f}</div>
                        <div class="metric-sub">Total bags required</div>
                    </div>
                </div>
                <div style="margin-top:0.75rem; background:var(--border); border-radius:4px; height:8px; overflow:hidden;">
                    <div style="width:{capex_fraction*100:.0f}%; height:100%; background:linear-gradient(90deg, var(--primary-dark), var(--primary)); border-radius:4px;"></div>
                </div>
                <div class="card-meta" style="margin-top:0.3rem;">{capex_fraction*100:.0f}% used · Remaining: {cement_bags_total - cement_bags_used:,.0f} bags</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Summary box
        st.markdown(
            f"""
            <div class="info-card" style="margin-top:0.75rem; border-left:4px solid var(--success);">
                <div class="card-title">📐 Project Summary</div>
                <div class="card-body" style="line-height:1.9;">
                    <b>Project:</b> {project_name if project_name else structure_type}<br/>
                    <b>Scale:</b> {builtup_sqft:,} sqft × {floors} floor(s) = {builtup_sqft*floors:,} sqft total<br/>
                    <b>Rate:</b> ₹{base_rate*tier_mult:,.0f} / sqft (post tier adjustment)<br/>
                    <b>Remaining Budget:</b> {_inr_format(total_budget_inr - capex_incurred)}<br/>
                    <b>ROI Potential:</b> {((market_valuation/capex_incurred)-1)*100:.1f}% on deployed capital
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        ) if completion_pct > 0 else None

    with col_right:
        # ── Milestone Progress Bar ────────────────────
        st.markdown(
            """
            <div class="section-header">
                <div class="section-icon">📅</div>
                <div><div class="section-title">Construction Milestone Progress</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Overall progress bar via Streamlit
        st.progress(completion_pct / 100)
        st.markdown(
            f'<div style="text-align:center; font-size:0.85rem; color:var(--text-muted); margin-top:-0.5rem; margin-bottom:0.75rem;">'
            f'<strong style="color:var(--primary);">{completion_pct}%</strong> Overall Project Completion</div>',
            unsafe_allow_html=True,
        )

        for threshold, stage_label in MILESTONE_STAGES:
            is_done = completion_pct >= threshold
            is_current = (completion_pct < threshold) and (
                next((t for t, _ in MILESTONE_STAGES if t > completion_pct), 100) == threshold
            )
            dot_color = "var(--success)" if is_done else ("var(--primary)" if is_current else "var(--border)")
            text_color = "var(--text-primary)" if is_done else ("var(--primary-light)" if is_current else "var(--text-dim)")
            status_text = "✅ Complete" if is_done else ("🔄 In Progress" if is_current else "⏳ Pending")

            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:0.75rem; padding:0.5rem 0.75rem;
                     background:{'rgba(16,185,129,0.06)' if is_done else ('rgba(249,115,22,0.08)' if is_current else 'transparent')};
                     border-radius:6px; margin-bottom:0.3rem;
                     border-left:3px solid {dot_color};">
                    <div style="font-size:0.85rem; color:{text_color}; flex:1;">{stage_label}</div>
                    <div style="font-size:0.7rem; color:{'var(--success)' if is_done else ('var(--primary)' if is_current else 'var(--text-dim)')};
                         font-weight:600; white-space:nowrap;">{status_text}</div>
                    <div style="font-size:0.7rem; color:var(--text-dim); font-family:monospace; white-space:nowrap;">{threshold}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── 3D Architectural Render ───────────────────────
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-header">
            <div class="section-icon">🏛️</div>
            <div>
                <div class="section-title">AI Architectural Concept Rendering</div>
                <div class="section-sub">Powered by Pollinations AI — photorealistic architectural visualization</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_prompt, col_render = st.columns([1, 1.5], gap="medium")

    with col_prompt:
        render_style = st.selectbox(
            "Rendering Style",
            ["Photorealistic Exterior", "Interior Lobby View", "Aerial Top-Down View", "Night Illuminated View", "Structural Blueprint Style"],
            key="render_style"
        )
        custom_prompt = st.text_area(
            "Custom Render Prompt (optional)",
            value="",
            key="render_prompt",
            placeholder="e.g. Glass curtain wall, tropical landscaping, rooftop garden",
            height=80
        )
        generate_btn = st.button("🎨 Generate Architectural Render", key="gen_render", use_container_width=True)

    with col_render:
        if generate_btn or "render_url" in st.session_state:
            if generate_btn:
                style_map = {
                    "Photorealistic Exterior": "modern photorealistic architectural exterior render, professional photography, golden hour lighting",
                    "Interior Lobby View": "luxury interior lobby render, high ceilings, marble floors, professional architectural photography",
                    "Aerial Top-Down View": "aerial architectural drone photograph, top-down view, urban context",
                    "Night Illuminated View": "architectural night render, dramatic lighting, glass facade, blue hour",
                    "Structural Blueprint Style": "architectural blueprint technical drawing, white lines on blue background, precise",
                }
                base_style = style_map.get(render_style, "")
                tier_label = location_tier.split("(")[0].strip()
                auto_prompt = (
                    f"{structure_type.lower()}, {floors}-story building, {tier_label} India, "
                    f"{base_style}"
                )
                if custom_prompt:
                    auto_prompt += f", {custom_prompt}"

                render_url = _get_pollinations_image_url(auto_prompt, width=800, height=500, seed=hash(auto_prompt) % 999)
                st.session_state["render_url"] = render_url
                st.session_state["render_prompt_used"] = auto_prompt

            if "render_url" in st.session_state:
                with st.spinner("🎨 Generating architectural visualization..."):
                    try:
                        resp = requests.get(st.session_state["render_url"], timeout=30)
                        if resp.status_code == 200:
                            st.image(
                                resp.content,
                                caption=f"AI Render: {render_style} — {structure_type}",
                                use_container_width=True
                            )
                            with st.expander("📋 View Render Prompt"):
                                st.code(st.session_state.get("render_prompt_used", ""), language="text")
                        else:
                            st.warning("⚠️ Could not load render. Try regenerating or check network.")
                    except Exception as e:
                        st.warning(f"⚠️ Render unavailable: {e}. Check network connectivity.")
        else:
            st.markdown(
                """
                <div class="info-card" style="text-align:center; padding:3rem 1rem; height:200px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                    <div style="font-size:2.5rem;">🏛️</div>
                    <div style="color:var(--text-muted); font-size:0.85rem; margin-top:0.5rem;">
                        Click <strong>Generate Architectural Render</strong><br/>to create an AI visualization
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
