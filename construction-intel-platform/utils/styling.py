"""
Custom CSS styling for the Multimodal Construction Intelligence Platform.
"""


def inject_custom_css():
    """Return the full custom CSS string for injection into Streamlit."""
    return """
<style>
    /* ─── Google Fonts ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ─── Root variables ────────────────────────────── */
    :root {
        --primary:       #F97316;
        --primary-light: #FB923C;
        --primary-dark:  #EA580C;
        --accent:        #38BDF8;
        --success:       #10B981;
        --warning:       #FBBF24;
        --danger:        #EF4444;
        --bg-base:       #0F172A;
        --bg-card:       #1E293B;
        --bg-card2:      #243044;
        --border:        #334155;
        --text-primary:  #F1F5F9;
        --text-muted:    #94A3B8;
        --text-dim:      #64748B;
        --radius:        12px;
        --radius-lg:     18px;
        --shadow:        0 4px 24px rgba(0,0,0,0.4);
    }

    /* ─── Base typography ───────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: var(--bg-base) !important;
        color: var(--text-primary) !important;
    }

    /* ─── Hide Streamlit default branding ───────────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ─── Scrollbar ─────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

    /* ─── Sidebar ───────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1B2E 0%, #0F172A 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .block-container { padding: 1rem 1rem !important; }

    /* ─── App header ────────────────────────────────── */
    .app-header {
        background: linear-gradient(135deg, #0D1B2E 0%, #1a2d4a 50%, #0D1B2E 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -10%;
        width: 50%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(249,115,22,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .app-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        right: 5%;
        width: 40%;
        height: 150%;
        background: radial-gradient(ellipse, rgba(56,189,248,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #F97316, #FB923C, #38BDF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        color: var(--text-muted);
        font-size: 0.9rem;
        font-weight: 400;
        margin: 0;
    }
    .app-badges {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .badge {
        background: rgba(249,115,22,0.15);
        border: 1px solid rgba(249,115,22,0.3);
        color: var(--primary-light);
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge.blue {
        background: rgba(56,189,248,0.12);
        border-color: rgba(56,189,248,0.3);
        color: var(--accent);
    }
    .badge.green {
        background: rgba(16,185,129,0.12);
        border-color: rgba(16,185,129,0.3);
        color: var(--success);
    }

    /* ─── Metric cards ──────────────────────────────── */
    .metric-grid {
        display: grid;
        gap: 1rem;
    }
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.2rem 1.5rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s, transform 0.2s;
    }
    .metric-card:hover { border-color: var(--primary); transform: translateY(-2px); }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: var(--radius) var(--radius) 0 0;
    }
    .metric-card.success::before { background: var(--success); }
    .metric-card.warning::before { background: var(--warning); }
    .metric-card.danger::before  { background: var(--danger); }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--text-dim);
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1;
        font-family: 'Inter', sans-serif;
    }
    .metric-value.primary { color: var(--primary); }
    .metric-value.success { color: var(--success); }
    .metric-value.warning { color: var(--warning); }
    .metric-value.danger  { color: var(--danger); }
    .metric-sub {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }

    /* ─── Status pills ──────────────────────────────── */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .status-pill.compliant   { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); }
    .status-pill.partial     { background: rgba(251,191,36,0.15);  color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }
    .status-pill.non-compliant { background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
    .status-pill.critical    { background: rgba(239,68,68,0.2);    color: #FCA5A5; border: 1px solid rgba(239,68,68,0.4); }
    .status-pill.high        { background: rgba(249,115,22,0.15);  color: #FB923C; border: 1px solid rgba(249,115,22,0.3); }
    .status-pill.medium      { background: rgba(251,191,36,0.12);  color: #FBBF24; border: 1px solid rgba(251,191,36,0.25); }
    .status-pill.low         { background: rgba(16,185,129,0.1);   color: #6EE7B7; border: 1px solid rgba(16,185,129,0.2); }

    /* ─── Info / content cards ──────────────────────── */
    .info-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
    }
    .info-card.hazard-critical { border-left: 4px solid var(--danger); }
    .info-card.hazard-high     { border-left: 4px solid var(--primary); }
    .info-card.hazard-medium   { border-left: 4px solid var(--warning); }
    .info-card.hazard-low      { border-left: 4px solid var(--success); }
    .card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .card-body {
        font-size: 0.85rem;
        color: var(--text-muted);
        line-height: 1.6;
    }
    .card-meta {
        font-size: 0.72rem;
        color: var(--text-dim);
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.4rem;
    }

    /* ─── Progress / Score ring ─────────────────────── */
    .score-ring-wrap {
        display: flex;
        align-items: center;
        gap: 2rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .score-circle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        flex-shrink: 0;
    }
    .score-number {
        font-size: 1.9rem;
        font-weight: 900;
        line-height: 1;
    }
    .score-label { font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }
    .score-info h3 { font-size: 1.1rem; font-weight: 700; margin: 0 0 0.3rem; }
    .score-info p  { font-size: 0.85rem; color: var(--text-muted); margin: 0; line-height: 1.5; }

    /* ─── Chat bubbles ──────────────────────────────── */
    .chat-msg {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1rem;
        align-items: flex-start;
    }
    .chat-msg.user { flex-direction: row-reverse; }
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .chat-avatar.user-av  { background: linear-gradient(135deg, var(--primary), var(--accent)); }
    .chat-avatar.bot-av   { background: linear-gradient(135deg, #1E293B, #243044); border: 1px solid var(--border); }
    .chat-bubble {
        max-width: 80%;
        padding: 0.75rem 1rem;
        border-radius: var(--radius);
        font-size: 0.88rem;
        line-height: 1.6;
    }
    .chat-bubble.user { background: linear-gradient(135deg, var(--primary-dark), var(--primary)); color: white; border-bottom-right-radius: 4px; }
    .chat-bubble.bot  { background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-bottom-left-radius: 4px; }

    /* ─── Section headers ───────────────────────────── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border);
    }
    .section-icon {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: rgba(249,115,22,0.15);
        border: 1px solid rgba(249,115,22,0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .section-title { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin: 0; }
    .section-sub   { font-size: 0.78rem; color: var(--text-dim); margin: 0; }

    /* ─── PPE checklist ─────────────────────────────── */
    .ppe-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.1rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .ppe-name { font-size: 0.9rem; font-weight: 600; }
    .ppe-note { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.15rem; }

    /* ─── Valuation cards ───────────────────────────── */
    .val-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
        text-align: center;
    }
    .val-amount {
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .val-currency { font-size: 1rem; font-weight: 600; color: var(--text-muted); }
    .val-label    { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); margin-top: 0.3rem; }

    /* ─── Demo mode banner ──────────────────────────── */
    .demo-banner {
        background: linear-gradient(135deg, rgba(249,115,22,0.1), rgba(56,189,248,0.08));
        border: 1px solid rgba(249,115,22,0.25);
        border-radius: var(--radius);
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        font-size: 0.82rem;
        color: var(--primary-light);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ─── Weather alert cards ───────────────────────── */
    .weather-alert {
        background: var(--bg-card);
        border-radius: var(--radius);
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
        border: 1px solid var(--border);
    }
    .weather-alert-title { font-size: 0.85rem; font-weight: 700; margin-bottom: 0.35rem; }
    .weather-alert-body  { font-size: 0.82rem; color: var(--text-muted); line-height: 1.55; }

    /* ─── Architecture vis card ─────────────────────── */
    .arch-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1rem;
        text-align: center;
    }
    .arch-card img { border-radius: 8px; max-width: 100%; }

    /* ─── Sidebar section titles ─────────────────────── */
    .sidebar-title {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-dim);
        margin: 1.2rem 0 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid var(--border);
    }

    /* ─── Streamlit widget overrides ────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 12px rgba(249,115,22,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(249,115,22,0.4) !important;
    }
    .stFileUploader > div {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius) !important;
    }
    .stSelectbox > div > div, .stTextArea > div > div > textarea, .stTextInput > div > div > input {
        background: var(--bg-card2) !important;
        border-color: var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    .stSlider > div[data-baseweb="slider"] > div:first-child { background: var(--border) !important; }
    .stSlider [data-baseweb="thumb"] { background: var(--primary) !important; border-color: var(--primary) !important; }
    div[data-testid="stTab"] button {
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    div[data-testid="stTab"] button[aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
    }
    .stSpinner > div > div { border-top-color: var(--primary) !important; }
    .stProgress > div > div > div > div { background: linear-gradient(90deg, var(--primary), var(--accent)) !important; }

    /* ─── Tooltip / expander ─────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* ─── JSON display ───────────────────────────────── */
    .json-block {
        background: #0D1B2E;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #7DD3FC;
        overflow-x: auto;
        max-height: 350px;
        overflow-y: auto;
    }

    /* ─── Responsive tweaks ──────────────────────────── */
    @media (max-width: 768px) {
        .app-title { font-size: 1.5rem; }
        .score-ring-wrap { flex-direction: column; text-align: center; }
        .metric-value { font-size: 1.6rem; }
    }
</style>
"""
