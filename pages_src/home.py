"""
pages_src/home.py — Landing / overview page
"""

import streamlit as st
from utils.model_loader import model_is_available, scaler_is_available, MODEL_PATHS, SCALER_PATH


def render():
    # ── Page header ──────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <h1>⚡ HAR70+ Activity Recognizer</h1>
            <p class="subtitle">
                Human Activity Recognition for Elderly Adults · Wearable Accelerometer Data
            </p>
            <div class="accent-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Model status cards ───────────────────────────────────────────
    st.markdown("<p class='section-header'>Model Status</p>", unsafe_allow_html=True)

    rf_ok     = model_is_available("Random Forest")
    svm_ok    = model_is_available("SVM (Linear)")
    scaler_ok = scaler_is_available()

    c1, c2, c3 = st.columns(3)
    with c1:
        status = "✅ Loaded" if rf_ok else "⚠️ Not Found"
        color  = "#3fb950" if rf_ok else "#d29922"
        st.markdown(
            f"""<div class="metric-card">
                    <div class="m-label">Random Forest</div>
                    <div class="m-value" style="font-size:1.1rem;color:{color};">{status}</div>
                    <div class="m-sub">models/random_forest.pkl</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        status = "✅ Loaded" if svm_ok else "⚠️ Not Found"
        color  = "#3fb950" if svm_ok else "#d29922"
        st.markdown(
            f"""<div class="metric-card">
                    <div class="m-label">SVM (Linear)</div>
                    <div class="m-value" style="font-size:1.1rem;color:{color};">{status}</div>
                    <div class="m-sub">models/svm_linear.pkl</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        status = "✅ Loaded" if scaler_ok else "⚠️ Not Found"
        color  = "#3fb950" if scaler_ok else "#d29922"
        st.markdown(
            f"""<div class="metric-card">
                    <div class="m-label">StandardScaler</div>
                    <div class="m-value" style="font-size:1.1rem;color:{color};">{status}</div>
                    <div class="m-sub">models/har_scaler.pkl</div>
                </div>""",
            unsafe_allow_html=True,
        )

    # ── Setup instructions if models missing ────────────────────────
    if not (rf_ok and svm_ok and scaler_ok):
        st.markdown(
            """
            <div class="warn-box">
                <strong>⚠️ Model files not found.</strong>
                Place your trained <code>.pkl</code> files inside the
                <code>har70_app/models/</code> folder and reload the app.
                See the setup guide below.
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("📋  Setup Guide — How to link your .pkl files"):
            st.markdown(
                """
                **Step 1 — Create the models folder** (if it doesn't exist):
                ```
                har70_app/
                └── models/
                    ├── random_forest.pkl    ← your trained RF model
                    ├── svm_linear.pkl       ← your trained SVM model
                    └── har_scaler.pkl       ← the StandardScaler from preprocessing
                ```

                **Step 2 — Copy your files:**
                - From your Downloads folder (or wherever you saved them)
                  copy the three `.pkl` files into `har70_app/models/`.

                **Step 3 — Reload the app:**
                - Press **R** in the browser, or click the ↻ icon in the top-right.

                **That's it!** The app caches the models so predictions are instant.
                """
            )

    # ── Dataset overview ────────────────────────────────────────────
    st.markdown("<p class='section-header'>Dataset Overview</p>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown(
            """
            <div class="info-box">
            The <strong>HAR70+</strong> dataset contains recordings from
            <strong>18 older adult participants</strong> (aged 70+) wearing two
            tri-axial Axivity AX3 accelerometers — one on the <strong>lower back</strong>
            and one on the <strong>right thigh</strong>. Data was recorded at
            <strong>50 Hz</strong> (50 samples per second) during 7 daily activities,
            annotated from synchronized video footage.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            """
            <div class="metric-row">
                <div class="metric-card">
                    <div class="m-label">Subjects</div>
                    <div class="m-value">18</div>
                    <div class="m-sub">Elderly adults 70+</div>
                </div>
                <div class="metric-card">
                    <div class="m-label">Frequency</div>
                    <div class="m-value">50Hz</div>
                    <div class="m-sub">Samples per second</div>
                </div>
            </div>
            <div class="metric-row">
                <div class="metric-card">
                    <div class="m-label">Sensors</div>
                    <div class="m-value">2</div>
                    <div class="m-sub">Back + Thigh</div>
                </div>
                <div class="metric-card">
                    <div class="m-label">Features</div>
                    <div class="m-value">42</div>
                    <div class="m-sub">Per 2-sec window</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Activity classes ────────────────────────────────────────────
    st.markdown("<p class='section-header'>Activity Classes</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="activity-grid">
            <div class="activity-chip">🚶 Walking</div>
            <div class="activity-chip">🐢 Shuffling</div>
            <div class="activity-chip">⬆️ Ascending Stairs</div>
            <div class="activity-chip">⬇️ Descending Stairs</div>
            <div class="activity-chip">🧍 Standing</div>
            <div class="activity-chip">🪑 Sitting</div>
            <div class="activity-chip">🛌 Lying Down</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Pipeline summary ────────────────────────────────────────────
    st.markdown("<p class='section-header'>Preprocessing Pipeline</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <ol class="pipeline-steps">
            <li>
                <div class="step-num">1</div>
                <div class="step-text">
                    <strong>Merge 18 CSVs</strong> — concatenate all subject files, inject
                    <code>subject_id</code> column
                </div>
            </li>
            <li>
                <div class="step-num">2</div>
                <div class="step-text">
                    <strong>Drop Timestamp</strong> — remove non-predictive clock column
                </div>
            </li>
            <li>
                <div class="step-num">3</div>
                <div class="step-text">
                    <strong>Sliding Windows</strong> — 100-row windows (2 sec) with 50% overlap
                </div>
            </li>
            <li>
                <div class="step-num">4</div>
                <div class="step-text">
                    <strong>Feature Extraction</strong> — 60 features: Mean, Std, MAD, Range,
                    Energy, ZCR, Entropy, SMA, Magnitude, Cross-axis Correlations
                </div>
            </li>
            <li>
                <div class="step-num">5</div>
                <div class="step-text">
                    <strong>SMOTE Balancing</strong> — K-NN synthetic oversampling on minority
                    classes (Stairs, Shuffling)
                </div>
            </li>
            <li>
                <div class="step-num">6</div>
                <div class="step-text">
                    <strong>StandardScaler</strong> — zero mean, unit variance normalization
                </div>
            </li>
        </ol>
        """,
        unsafe_allow_html=True,
    )
