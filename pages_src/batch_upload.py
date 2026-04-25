"""
pages_src/batch_upload.py
CSV batch prediction page — upload a file, get predictions for every row/window.
"""

import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.feature_extractor import extract_features, FEATURE_NAMES
from utils.predictor import run_prediction, render_probability_chart
from utils.model_loader import (
    load_model, load_scaler, model_is_available, scaler_is_available,
    LABEL_MAP, ACTIVITY_COLORS, ACTIVITY_ICONS,
)

SENSOR_COLS = ["back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z"]
WINDOW_SIZE = 100
STEP_SIZE   = 50


def render():
    # ── Page header ──────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <h1>📂 Batch CSV Prediction</h1>
            <p class="subtitle">
                Upload a raw accelerometer CSV file and get activity predictions for every window.
            </p>
            <div class="accent-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_name = st.session_state.get("selected_model", "Random Forest")

    # ── Expected format guide ────────────────────────────────────────
    with st.expander("📋  Expected CSV Format"):
        st.markdown(
            """
            Your CSV must have at minimum these **6 sensor columns** (column names are case-sensitive):

            | back_x | back_y | back_z | thigh_x | thigh_y | thigh_z |
            |--------|--------|--------|---------|---------|---------|
            | 0.02   | -0.01  | 0.98   | 0.01    | -0.02   | 0.99   |

            **Optional columns** (they are ignored during prediction):
            - `timestamp` — any format, will be dropped automatically
            - `label` — if present, the app will show a prediction vs ground-truth comparison
            - `subject_id` — ignored

            **Minimum rows:** At least **100 rows** are needed to form one window.
            At 50 Hz, this equals **2 seconds** of recording.
            """
        )
        # Show a sample CSV download button
        sample_data = pd.DataFrame(
            np.random.uniform(-0.5, 0.5, (200, 6)) + np.array([0, 0, 1, 0, 0, 1]),
            columns=SENSOR_COLS,
        ).round(4)
        sample_csv = sample_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Sample CSV",
            data=sample_csv,
            file_name="sample_sensor_data.csv",
            mime="text/csv",
        )

    # ── File upload ──────────────────────────────────────────────────
    st.markdown("<p class='section-header'>Upload Sensor Data</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Drop your CSV file here",
        type=["csv"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.markdown(
            """<div class="info-box">
            Upload a CSV file above to begin batch prediction.
            The app will automatically segment the data into 2-second windows
            with 50% overlap and run the selected model on each window.
            </div>""",
            unsafe_allow_html=True,
        )
        return

    # ── Parse uploaded CSV ───────────────────────────────────────────
    try:
        df_raw = pd.read_csv(uploaded_file)
    except Exception as e:
        st.markdown(f'<div class="error-box"><strong>CSV parse error:</strong> {e}</div>',
                    unsafe_allow_html=True)
        return

    # Drop timestamp-like columns
    time_cols = [c for c in df_raw.columns if "time" in c.lower() or "date" in c.lower()]
    if time_cols:
        df_raw.drop(columns=time_cols, inplace=True)

    # Check that all required sensor columns are present
    missing_cols = [c for c in SENSOR_COLS if c not in df_raw.columns]
    if missing_cols:
        st.markdown(
            f'<div class="error-box"><strong>Missing columns:</strong> {missing_cols}<br>'
            f'Your file has: {list(df_raw.columns)}</div>',
            unsafe_allow_html=True,
        )
        return

    if len(df_raw) < WINDOW_SIZE:
        st.markdown(
            f'<div class="error-box"><strong>Too few rows:</strong> File has {len(df_raw)} rows. '
            f'Minimum required is {WINDOW_SIZE} rows (= 1 window).</div>',
            unsafe_allow_html=True,
        )
        return

    # ── Show data preview ────────────────────────────────────────────
    st.markdown("<p class='section-header'>Data Preview</p>", unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(
            f"""<div class="metric-card">
                    <div class="m-label">Total Rows</div>
                    <div class="m-value">{len(df_raw):,}</div>
                    <div class="m-sub">~{len(df_raw)/50:.1f} seconds of data</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with col_m2:
        n_windows = max(0, (len(df_raw) - WINDOW_SIZE) // STEP_SIZE + 1)
        st.markdown(
            f"""<div class="metric-card">
                    <div class="m-label">Windows</div>
                    <div class="m-value">{n_windows:,}</div>
                    <div class="m-sub">100 rows / 50% overlap</div>
                </div>""",
            unsafe_allow_html=True,
        )
    with col_m3:
        has_labels = "label" in df_raw.columns
        st.markdown(
            f"""<div class="metric-card">
                    <div class="m-label">Ground Truth</div>
                    <div class="m-value">{'✅ Yes' if has_labels else '—'}</div>
                    <div class="m-sub">{'label column found' if has_labels else 'No label column'}</div>
                </div>""",
            unsafe_allow_html=True,
        )

    st.dataframe(df_raw.head(10), use_container_width=True)

    # ── Run Predictions button ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, _ = st.columns([2, 5])
    with btn_col:
        run_clicked = st.button("⚡  RUN BATCH PREDICTION", use_container_width=True)

    if not run_clicked:
        return

    # ── Model availability ───────────────────────────────────────────
    if not model_is_available(model_name):
        st.markdown(
            f'<div class="error-box"><strong>Model not found:</strong> '
            f'Add the .pkl file to models/ and reload.</div>',
            unsafe_allow_html=True,
        )
        return

    model  = load_model(model_name)
    scaler = load_scaler()

    # ── Windowing & feature extraction ──────────────────────────────
    sensor_data  = df_raw[SENSOR_COLS].values
    true_labels  = df_raw["label"].values if has_labels else None

    windows_feat  = []
    windows_labels = []
    window_indices = []

    progress_bar = st.progress(0, text="Extracting features from windows...")
    total_windows = max(1, (len(sensor_data) - WINDOW_SIZE) // STEP_SIZE + 1)

    for i, start in enumerate(range(0, len(sensor_data) - WINDOW_SIZE + 1, STEP_SIZE)):
        end    = start + WINDOW_SIZE
        window = sensor_data[start:end]
        feat   = extract_features(window)
        windows_feat.append(feat)
        window_indices.append(start)

        # Majority-vote label from ground truth if available
        if true_labels is not None:
            win_labs = true_labels[start:end]
            majority = pd.Series(win_labs).mode()[0]
            windows_labels.append(int(majority))

        progress_bar.progress((i + 1) / total_windows, text=f"Processing window {i+1}/{total_windows}...")

    progress_bar.empty()

    X = np.array(windows_feat, dtype=np.float32)
    if scaler is not None:
        X_scaled = scaler.transform(X)
    else:
        X_scaled = X

    # ── Predictions ──────────────────────────────────────────────────
    predictions = model.predict(X_scaled)
    pred_labels = [int(p) for p in predictions]
    pred_names  = [LABEL_MAP.get(p, str(p)) for p in pred_labels]

    # Probabilities — RF uses predict_proba directly
    # SVM uses decision_function + softmax to approximate probabilities
    if hasattr(model, "predict_proba"):
        proba_matrix = model.predict_proba(X_scaled)
        max_probs    = proba_matrix.max(axis=1)

    elif hasattr(model, "decision_function"):
        scores = model.decision_function(X_scaled)
        if scores.ndim == 1:
            scores = scores.reshape(-1, 1)
        scores_shifted = scores - scores.max(axis=1, keepdims=True)
        exp_scores     = np.exp(scores_shifted)
        proba_matrix   = exp_scores / exp_scores.sum(axis=1, keepdims=True)
        max_probs      = proba_matrix.max(axis=1)

    else:
        proba_matrix = None
        max_probs    = [None] * len(pred_labels)

    # ── Build results DataFrame ──────────────────────────────────────
    results_df = pd.DataFrame({
        "Window #"           : range(1, len(pred_labels) + 1),
        "Start Row"          : window_indices,
        "Predicted Activity" : pred_names,
        "Pred Label"         : pred_labels,
        "Confidence"         : [f"{p*100:.1f}%" if p is not None else "N/A" for p in max_probs],
    })

    if windows_labels:
        results_df["True Activity"] = [LABEL_MAP.get(l, str(l)) for l in windows_labels]
        results_df["True Label"]    = windows_labels
        results_df["Correct"]       = results_df["Pred Label"] == results_df["True Label"]

    # ── Summary metrics ──────────────────────────────────────────────
    st.markdown("<p class='section-header'>Prediction Results</p>", unsafe_allow_html=True)

    sm1, sm2, sm3, sm4 = st.columns(4)
    with sm1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="m-label">Total Windows</div>
                <div class="m-value">{len(pred_labels):,}</div>
            </div>""", unsafe_allow_html=True,
        )
    with sm2:
        most_common_act = pd.Series(pred_names).value_counts().index[0]
        st.markdown(
            f"""<div class="metric-card">
                <div class="m-label">Dominant Activity</div>
                <div class="m-value" style="font-size:0.9rem;">{ACTIVITY_ICONS.get(most_common_act,'')}&nbsp;{most_common_act}</div>
            </div>""", unsafe_allow_html=True,
        )
    with sm3:
        if proba_matrix is not None:
            avg_conf = np.mean(max_probs) * 100
            st.markdown(
                f"""<div class="metric-card">
                    <div class="m-label">Avg Confidence</div>
                    <div class="m-value">{avg_conf:.1f}%</div>
                </div>""", unsafe_allow_html=True,
            )
    with sm4:
        if windows_labels:
            acc = results_df["Correct"].mean() * 100
            st.markdown(
                f"""<div class="metric-card">
                    <div class="m-label">Accuracy</div>
                    <div class="m-value" style="color:#3fb950;">{acc:.1f}%</div>
                    <div class="m-sub">vs ground truth</div>
                </div>""", unsafe_allow_html=True,
            )

    # ── Tabs: table / timeline / distribution ────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋  Predictions Table", "📈  Activity Timeline", "🥧  Distribution"])

    with tab1:
        st.dataframe(results_df, use_container_width=True, height=400)

        # Download predictions
        csv_out = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Predictions CSV",
            data=csv_out,
            file_name="har_predictions.csv",
            mime="text/csv",
        )

    with tab2:
        # Map activity names to numeric codes for plotting
        activity_to_code = {v: k for k, v in LABEL_MAP.items()}
        y_pred_codes = [activity_to_code.get(a, 0) for a in pred_names]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(pred_labels) + 1)),
            y=y_pred_codes,
            mode="lines+markers",
            marker=dict(size=4, color=[ACTIVITY_COLORS.get(a, "#58a6ff") for a in pred_names]),
            line=dict(color="#58a6ff", width=1.5),
            name="Predicted",
        ))

        if windows_labels:
            fig.add_trace(go.Scatter(
                x=list(range(1, len(windows_labels) + 1)),
                y=windows_labels,
                mode="lines",
                line=dict(color="#8b949e", width=1, dash="dot"),
                name="Ground Truth",
            ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(28,35,51,0.6)",
            font=dict(family="DM Sans", color="#e6edf3"),
            yaxis=dict(
                tickvals=list(LABEL_MAP.keys()),
                ticktext=list(LABEL_MAP.values()),
                gridcolor="#30363d",
            ),
            xaxis=dict(title="Window #", gridcolor="#30363d"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=30, b=10),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        counts = pd.Series(pred_names).value_counts()
        fig2 = go.Figure(go.Bar(
            x=counts.index.tolist(),
            y=counts.values.tolist(),
            marker_color=[ACTIVITY_COLORS.get(a, "#58a6ff") for a in counts.index],
            marker_line_width=0,
            text=[f"{v}" for v in counts.values],
            textposition="outside",
            textfont=dict(color="#e6edf3"),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(28,35,51,0.6)",
            font=dict(family="DM Sans", color="#e6edf3"),
            xaxis=dict(gridcolor="#30363d"),
            yaxis=dict(title="Window Count", gridcolor="#30363d"),
            margin=dict(l=10, r=10, t=30, b=10),
            height=320,
            title=dict(text="Predicted Activity Distribution", font=dict(size=12, color="#8b949e"), x=0),
        )
        st.plotly_chart(fig2, use_container_width=True)