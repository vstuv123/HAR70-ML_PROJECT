"""
utils/styles.py
Injects custom CSS into the Streamlit app for a polished, consistent design.
"""

import streamlit as st

CSS = """
<style>
/* ─── Google Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ─── Root Variables ─── */
:root {
    --bg-primary:    #0d1117;
    --bg-secondary:  #161b22;
    --bg-card:       #1c2333;
    --bg-card-hover: #21293a;
    --border:        #30363d;
    --accent:        #58a6ff;
    --accent-glow:   rgba(88, 166, 255, 0.15);
    --accent-green:  #3fb950;
    --accent-orange: #d29922;
    --accent-red:    #f85149;
    --text-primary:  #e6edf3;
    --text-muted:    #8b949e;
    --text-dim:      #484f58;
    --radius:        10px;
    --font-mono:     'Space Mono', monospace;
    --font-body:     'DM Sans', sans-serif;
}

/* ─── Global ─── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ─── Hide Streamlit chrome ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── App container ─── */
.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1100px;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1.2rem !important; }

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.2rem;
}
.brand-icon { font-size: 1.6rem; }
.brand-text {
    font-family: var(--font-mono);
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 2px;
}
.sidebar-tagline {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
    margin-left: 2.2rem;
}
.nav-divider {
    border-top: 1px solid var(--border);
    margin: 0.8rem 0;
}
.sidebar-section-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.4rem;
}
.model-path-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
}
.model-path-label code {
    background: var(--bg-card);
    padding: 1px 5px;
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--accent-green);
}
.sidebar-footer {
    font-size: 0.65rem;
    color: var(--text-dim);
    text-align: center;
    letter-spacing: 0.5px;
}

/* ─── Radio nav buttons ─── */
[data-testid="stSidebar"] .stRadio label {
    display: block;
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius);
    font-size: 0.88rem;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.15s ease;
    margin: 2px 0;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg-card);
    color: var(--text-primary);
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label,
[data-testid="stSidebar"] .stRadio input:checked + div label {
    background: var(--accent-glow);
    color: var(--accent);
    border: 1px solid rgba(88,166,255,0.3);
}

/* ─── Page title block ─── */
.page-header {
    margin-bottom: 2rem;
}
.page-header h1 {
    font-family: var(--font-mono);
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin: 0 0 0.3rem 0;
}
.page-header .subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin: 0;
}
.accent-bar {
    width: 48px;
    height: 3px;
    background: var(--accent);
    border-radius: 2px;
    margin: 0.7rem 0 0 0;
}

/* ─── Metric Cards ─── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    flex: 1;
    min-width: 130px;
}
.metric-card .m-label {
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.3rem;
}
.metric-card .m-value {
    font-family: var(--font-mono);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-card .m-sub {
    font-size: 0.72rem;
    color: var(--text-dim);
    margin-top: 0.1rem;
}

/* ─── Result Banner ─── */
.result-banner {
    background: linear-gradient(135deg, var(--bg-card) 0%, #1e2d40 100%);
    border: 1px solid rgba(88,166,255,0.3);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.4rem 1.8rem;
    margin: 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 1.2rem;
}
.result-icon { font-size: 2.5rem; }
.result-body .r-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.result-body .r-activity {
    font-family: var(--font-mono);
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}
.result-body .r-confidence {
    font-size: 0.85rem;
    color: var(--accent-green);
    font-weight: 600;
}

/* ─── Info / Warning boxes ─── */
.info-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: 0.9rem 1.1rem;
    font-size: 0.85rem;
    color: var(--text-muted);
    margin: 0.8rem 0;
    line-height: 1.6;
}
.warn-box {
    background: rgba(210, 153, 34, 0.08);
    border: 1px solid rgba(210, 153, 34, 0.3);
    border-left: 3px solid var(--accent-orange);
    border-radius: var(--radius);
    padding: 0.9rem 1.1rem;
    font-size: 0.85rem;
    color: var(--accent-orange);
    margin: 0.8rem 0;
}
.error-box {
    background: rgba(248, 81, 73, 0.08);
    border: 1px solid rgba(248, 81, 73, 0.3);
    border-left: 3px solid var(--accent-red);
    border-radius: var(--radius);
    padding: 0.9rem 1.1rem;
    font-size: 0.85rem;
    color: var(--accent-red);
    margin: 0.8rem 0;
}

/* ─── Section headers ─── */
.section-header {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
    margin: 1.8rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* ─── Streamlit widgets ─── */
.stSlider > div > div > div > div { background: var(--accent) !important; }
.stNumberInput input, .stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
}
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #79b8ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(88,166,255,0.3) !important;
}
.stDataFrame { border: 1px solid var(--border) !important; border-radius: var(--radius) !important; }
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}
.stProgress > div > div { background-color: var(--bg-card) !important; }
.stProgress > div > div > div { background-color: var(--accent) !important; }

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    padding: 0.6rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ─── Home page activity grid ─── */
.activity-grid { display: flex; flex-wrap: wrap; gap: 0.8rem; margin: 1rem 0; }
.activity-chip {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    font-size: 0.82rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ─── Pipeline step list ─── */
.pipeline-steps { counter-reset: step; list-style: none; padding: 0; }
.pipeline-steps li {
    counter-increment: step;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--border);
}
.pipeline-steps li:last-child { border-bottom: none; }
.step-num {
    background: var(--accent-glow);
    border: 1px solid rgba(88,166,255,0.4);
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 0.75rem;
    font-weight: 700;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.step-text { font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; }
.step-text strong { color: var(--text-primary); }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
