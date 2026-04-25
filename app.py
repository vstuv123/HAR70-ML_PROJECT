"""
HAR70+ Activity Recognition — Streamlit Web Application
Entry point: run with `streamlit run app.py`
"""
 
import streamlit as st
 
# Page config MUST be the very first Streamlit call
st.set_page_config(
    page_title="HAR70+ Activity Recognizer",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# Import page modules
from pages_src import home, manual_input, batch_upload, about
from utils.styles import inject_css
 
# Inject global CSS styling
inject_css()
 
# ──────────────────────────────────────────────────────────────────────────────
# Top Navigation Bar — replaces sidebar so nothing can hide it
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="topbar">
        <div class="topbar-brand">
            <span class="brand-icon">⚡</span>
            <span class="brand-text">HAR70+</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
 
# Navigation + model selector in one row
nav_col1, nav_col2, nav_col3, nav_col4, spacer, model_col = st.columns([1.2, 1.2, 1.2, 1.2, 2, 2])
 
with nav_col1:
    home_btn = st.button("🏠  Home", use_container_width=True, key="nav_home")
with nav_col2:
    manual_btn = st.button("🎛️  Manual Input", use_container_width=True, key="nav_manual")
with nav_col3:
    batch_btn = st.button("📂  Batch Upload", use_container_width=True, key="nav_batch")
with nav_col4:
    about_btn = st.button("ℹ️  About", use_container_width=True, key="nav_about")
with model_col:
    selected_model = st.selectbox(
        label="🤖  Active Model",
        options=["Random Forest", "SVM (Linear)"],
        index=0,
        key="model_select",
    )
    st.session_state["selected_model"] = selected_model
 
st.markdown("<div class='topnav-divider'></div>", unsafe_allow_html=True)
 
# ──────────────────────────────────────────────────────────────────────────────
# Page state management
# ──────────────────────────────────────────────────────────────────────────────
 
# Set default page on first load
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"
 
# Update page based on which button was clicked
if home_btn:
    st.session_state["current_page"] = "home"
if manual_btn:
    st.session_state["current_page"] = "manual"
if batch_btn:
    st.session_state["current_page"] = "batch"
if about_btn:
    st.session_state["current_page"] = "about"
 
# ──────────────────────────────────────────────────────────────────────────────
# Page Router
# ──────────────────────────────────────────────────────────────────────────────
page = st.session_state["current_page"]
 
if page == "home":
    home.render()
elif page == "manual":
    manual_input.render()
elif page == "batch":
    batch_upload.render()
elif page == "about":
    about.render()