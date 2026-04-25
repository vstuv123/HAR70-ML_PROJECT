"""
pages_src/about.py — About / documentation page
"""

import streamlit as st


def render():
    st.markdown(
        """
        <div class="page-header">
            <h1>ℹ️ About This Application</h1>
            <p class="subtitle">Technical documentation, model details, and deployment guide.</p>
            <div class="accent-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["🏗️  Architecture", "🤖  Models", "🚀  Deployment"])

    with tab1:
        st.markdown("<p class='section-header'>Project Structure</p>", unsafe_allow_html=True)
        st.code(
            """
har70_app/
├── app.py                     ← Main entry point (run this with streamlit)
│
├── pages_src/
│   ├── __init__.py
│   ├── home.py                ← Landing page with dataset overview
│   ├── manual_input.py        ← Slider/number field prediction
│   ├── batch_upload.py        ← CSV upload and batch prediction
│   └── about.py               ← This page
│
├── utils/
│   ├── __init__.py
│   ├── model_loader.py        ← Loads .pkl files with caching
│   ├── feature_extractor.py   ← 60-feature extraction (mirrors preprocessing)
│   ├── predictor.py           ← Shared prediction + chart rendering logic
│   └── styles.py              ← All custom CSS injected into Streamlit
│
├── models/                    ← ⬅ Place your .pkl files here
│   ├── random_forest.pkl
│   ├── svm_linear.pkl
│   └── har_scaler.pkl
│
└── requirements.txt           ← Python dependencies
            """,
            language="",
        )

        st.markdown("<p class='section-header'>Feature Engineering Pipeline</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-box">
            The app extracts the same 60 features per window that were used during model training.
            Features are grouped into four categories:
            <br><br>
            <strong>Statistical (8 × 6 axes = 48):</strong>
            Mean, Std Dev, Median, MAD, Range, Energy, Zero-Crossing Rate, Entropy
            <br><br>
            <strong>Magnitude (4):</strong>
            Back magnitude mean/std, Thigh magnitude mean/std (√x²+y²+z²)
            <br><br>
            <strong>SMA (2):</strong>
            Signal Magnitude Area for back sensor and thigh sensor
            <br><br>
            <strong>Correlations (6):</strong>
            Pearson cross-axis correlations within back sensor (xy, xz, yz)
            and within thigh sensor (xy, xz, yz)
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown("<p class='section-header'>Model Comparison</p>", unsafe_allow_html=True)

        col_rf, col_svm = st.columns(2)
        with col_rf:
            st.markdown(
                """
                <div class="metric-card" style="min-height:200px;">
                    <div class="m-label">Random Forest</div>
                    <div class="m-value" style="font-size:1rem;margin-top:0.3rem;">🌲 Ensemble Model</div>
                    <br>
                    <div class="step-text">
                        <strong>Strengths:</strong> Handles noisy elderly sensor data well,
                        no scaling required, outputs calibrated probabilities, robust to
                        correlated features.<br><br>
                        <strong>When to use:</strong> General purpose, best starting model
                        for HAR tasks.<br><br>
                        <strong>Needs scaling:</strong> No (but applied anyway for consistency)
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_svm:
            st.markdown(
                """
                <div class="metric-card" style="min-height:200px;">
                    <div class="m-label">SVM (Linear)</div>
                    <div class="m-value" style="font-size:1rem;margin-top:0.3rem;">📐 Margin Classifier</div>
                    <br>
                    <div class="step-text">
                        <strong>Strengths:</strong> Excellent at finding clean separation between
                        clearly different activities (Sitting vs Walking), handles high-dimensional
                        feature spaces well.<br><br>
                        <strong>When to use:</strong> When activity boundaries are well-defined
                        and the dataset is balanced.<br><br>
                        <strong>Needs scaling:</strong> <strong style="color:#f85149;">Yes — essential</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-box">
            <strong>Note on Probability Scores with SVM:</strong> Unlike Random Forest,
            a linear SVM does not natively output calibrated probabilities.
            This app uses a <strong>softmax transformation on the decision function scores</strong>
            to produce approximate probability-like values for the probability bar chart.
            These are <em>indicative</em>, not strictly calibrated probabilities.
            If you trained your SVM with <code>probability=True</code> in scikit-learn,
            proper Platt-scaled probabilities will be used automatically.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown("<p class='section-header'>Local Development</p>", unsafe_allow_html=True)
        st.code(
            """
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place your .pkl files in models/
#    har70_app/models/random_forest.pkl
#    har70_app/models/svm_linear.pkl
#    har70_app/models/har_scaler.pkl

# 3. Run the app
cd har70_app
streamlit run app.py
            """,
            language="bash",
        )

        st.markdown("<p class='section-header'>Deploy on Streamlit Community Cloud (Free)</p>",
                    unsafe_allow_html=True)
        st.markdown(
            """
            <ol class="pipeline-steps">
                <li>
                    <div class="step-num">1</div>
                    <div class="step-text">
                        Push this project folder to a <strong>GitHub repository</strong>.
                    </div>
                </li>
                <li>
                    <div class="step-num">2</div>
                    <div class="step-text">
                        Go to <strong>share.streamlit.io</strong> and sign in with GitHub.
                    </div>
                </li>
                <li>
                    <div class="step-num">3</div>
                    <div class="step-text">
                        Click <strong>New App</strong>, select your repo, set
                        <strong>Main file path</strong> to <code>har70_app/app.py</code>.
                    </div>
                </li>
                <li>
                    <div class="step-num">4</div>
                    <div class="step-text">
                        Make sure <code>requirements.txt</code> is present in the repo root
                        — Streamlit Cloud installs from it automatically.
                    </div>
                </li>
                <li>
                    <div class="step-num">5</div>
                    <div class="step-text">
                        <strong>Model files:</strong> Commit the <code>models/</code> folder
                        to GitHub (if files are under 100 MB), or use
                        <strong>Streamlit Secrets</strong> / cloud storage for larger models.
                    </div>
                </li>
            </ol>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<p class='section-header'>Deploy on Heroku / Railway / Render</p>",
                    unsafe_allow_html=True)
        st.code(
            """
# Procfile (place in repo root)
web: streamlit run har70_app/app.py --server.port=$PORT --server.address=0.0.0.0
            """,
            language="",
        )
