"""
utils/model_loader.py
Handles loading of pre-trained model .pkl files and the StandardScaler.

HOW TO LINK YOUR MODELS:
1. Copy your trained model files into the  har70_app/models/  folder:
       har70_app/
       ├── models/
       │   ├── random_forest.pkl   ← your Random Forest model
       │   ├── svm_linear.pkl      ← your SVM (Linear) model
       │   └── har_scaler.pkl      ← the StandardScaler fitted during preprocessing
2. That's it — the app will automatically pick them up.
"""

import os
import joblib
import streamlit as st

# ──────────────────────────────────────────────
# Paths — relative to the project root (har70_app/)
# If your pkl files live somewhere else, update these paths.
# ──────────────────────────────────────────────
MODEL_PATHS = {
    "Random Forest": os.path.join("models", "har70_rf_model.pkl"),
    "SVM (Linear)":  os.path.join("models", "har70_svm_model.pkl"),
}

SCALER_PATH = os.path.join("models", "har70_scaler.pkl")

# ──────────────────────────────────────────────
# Activity label mapping
# ──────────────────────────────────────────────
LABEL_MAP = {
    1: "Walking",
    3: "Shuffling",
    4: "Ascending Stairs",
    5: "Descending Stairs",
    6: "Standing",
    7: "Sitting",
    8: "Lying Down",
}

# Nice emoji icons for each activity (used in the UI)
ACTIVITY_ICONS = {
    "Walking":           "🚶",
    "Shuffling":         "🐢",
    "Ascending Stairs":  "⬆️",
    "Descending Stairs": "⬇️",
    "Standing":          "🧍",
    "Sitting":           "🪑",
    "Lying Down":        "🛌",
}

# Colour codes for the probability bar chart
ACTIVITY_COLORS = {
    "Walking":           "#2196F3",
    "Shuffling":         "#FF9800",
    "Ascending Stairs":  "#4CAF50",
    "Descending Stairs": "#F44336",
    "Standing":          "#9C27B0",
    "Sitting":           "#00BCD4",
    "Lying Down":        "#795548",
}


@st.cache_resource(show_spinner=False)
def load_model(model_name: str):
    """
    Load a pickled scikit-learn model from disk.
    Uses Streamlit's @cache_resource so the model is loaded only once
    per session (fast subsequent predictions).

    Returns the model object, or None if the file is not found.
    """
    path = MODEL_PATHS.get(model_name)
    if path is None:
        return None
    if not os.path.exists(path):
        return None
    try:
        model = joblib.load(path)
        return model
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_scaler():
    """
    Load the pre-fitted StandardScaler from disk.
    This MUST be the same scaler used during training — otherwise
    the feature values will be on the wrong scale and predictions will be wrong.

    Returns the scaler object, or None if the file is not found.
    """
    if not os.path.exists(SCALER_PATH):
        return None
    try:
        scaler = joblib.load(SCALER_PATH)
        return scaler
    except Exception:
        return None


def model_is_available(model_name: str) -> bool:
    """Return True if the pkl file for this model exists on disk."""
    path = MODEL_PATHS.get(model_name, "")
    return os.path.exists(path)


def scaler_is_available() -> bool:
    """Return True if the scaler pkl file exists on disk."""
    return os.path.exists(SCALER_PATH)
