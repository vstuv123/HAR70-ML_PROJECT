"""
utils/predictor.py
Shared prediction logic used by both the Manual Input and Batch Upload pages.
"""

import numpy as np
import pandas as pd
import streamlit as st

from utils.model_loader import load_model, load_scaler, LABEL_MAP, ACTIVITY_ICONS, ACTIVITY_COLORS


def run_prediction(feature_vector: np.ndarray, model_name: str) -> dict | None:
    """
    Run a prediction on a single pre-extracted feature vector.

    Parameters
    ----------
    feature_vector : np.ndarray, shape (1, n_features)
    model_name     : str — must match a key in MODEL_PATHS

    Returns
    -------
    dict with keys:
        predicted_label    : int
        predicted_activity : str
        confidence         : float (0–1)
        probabilities      : dict {activity_name: probability}  (if model supports predict_proba)
        activity_icon      : str emoji
    or None if model / scaler is not loaded.
    """
    model  = load_model(model_name)
    scaler = load_scaler()

    if model is None:
        return None

    # Scale the features if scaler is available
    if scaler is not None:
        X = scaler.transform(feature_vector)
    else:
        X = feature_vector

    # Predict class label
    pred_label = int(model.predict(X)[0])
    pred_activity = LABEL_MAP.get(pred_label, f"Unknown ({pred_label})")

    # Confidence / probability
    probabilities = {}
    confidence = None

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0]
        classes = model.classes_

        for cls, prob in zip(classes, proba):
            act_name = LABEL_MAP.get(int(cls), str(cls))
            probabilities[act_name] = float(prob)

        confidence = float(probabilities.get(pred_activity, 0.0))

    elif hasattr(model, "decision_function"):
        # SVM without probability calibration — use softmax on decision scores
        scores = model.decision_function(X)[0]
        if scores.ndim == 0:
            scores = np.array([scores])
        exp_scores = np.exp(scores - scores.max())
        softmax    = exp_scores / exp_scores.sum()
        classes    = model.classes_

        for cls, prob in zip(classes, softmax):
            act_name = LABEL_MAP.get(int(cls), str(cls))
            probabilities[act_name] = float(prob)

        confidence = float(probabilities.get(pred_activity, 0.0))

    return {
        "predicted_label"   : pred_label,
        "predicted_activity": pred_activity,
        "confidence"        : confidence,
        "probabilities"     : probabilities,
        "activity_icon"     : ACTIVITY_ICONS.get(pred_activity, "❓"),
        "activity_colors"   : ACTIVITY_COLORS,
    }


def render_result_banner(result: dict):
    """Render the large prediction result banner."""
    conf_str = f"{result['confidence'] * 100:.1f}% confidence" if result["confidence"] is not None else ""
    st.markdown(
        f"""
        <div class="result-banner">
            <div class="result-icon">{result['activity_icon']}</div>
            <div class="result-body">
                <div class="r-label">Predicted Activity</div>
                <div class="r-activity">{result['predicted_activity']}</div>
                <div class="r-confidence">{conf_str}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probability_chart(result: dict):
    """Render the Plotly horizontal bar chart of class probabilities."""
    if not result["probabilities"]:
        st.info("This model does not support probability scores.")
        return

    import plotly.graph_objects as go

    probs = result["probabilities"]
    # Sort descending by probability
    sorted_items = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    activities   = [item[0] for item in sorted_items]
    values       = [item[1] * 100 for item in sorted_items]
    colors_list  = [result["activity_colors"].get(act, "#58a6ff") for act in activities]

    fig = go.Figure(go.Bar(
        x=values,
        y=activities,
        orientation="h",
        marker_color=colors_list,
        marker_line_width=0,
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(color="#e6edf3", size=11),
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(28, 35, 51, 0.6)",
        font=dict(family="DM Sans", color="#e6edf3"),
        xaxis=dict(
            range=[0, 110],
            ticksuffix="%",
            gridcolor="#30363d",
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            tickfont=dict(size=11),
            automargin=True,
        ),
        margin=dict(l=10, r=40, t=30, b=10),
        height=300,
        bargap=0.3,
        title=dict(
            text="Probability Distribution Across All Activity Classes",
            font=dict(size=12, color="#8b949e"),
            x=0,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)
