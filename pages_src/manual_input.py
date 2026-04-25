"""
pages_src/manual_input.py
Manual sensor value input page — enter values via sliders or number fields,
get immediate activity prediction with probability chart.
"""

import numpy as np
import streamlit as st

from utils.feature_extractor import extract_features_from_single_input
from utils.predictor import run_prediction, render_result_banner, render_probability_chart
from utils.model_loader import model_is_available, scaler_is_available


def render():
    # ── Page header ──────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <h1>🎛️ Manual Sensor Input</h1>
            <p class="subtitle">
                Enter accelerometer values manually and get an instant activity prediction.
            </p>
            <div class="accent-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_name = st.session_state.get("selected_model", "Random Forest")

    # ── Model availability check ─────────────────────────────────────
    if not model_is_available(model_name):
        st.markdown(
            f"""
            <div class="warn-box">
                <strong>⚠️ {model_name} model not found.</strong>
                Add <code>models/{'random_forest' if 'Forest' in model_name else 'svm_linear'}.pkl</code>
                to the project folder and reload.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not scaler_is_available():
        st.markdown(
            """<div class="warn-box">
                <strong>⚠️ Scaler (har_scaler.pkl) not found.</strong>
                Predictions will run without feature scaling — accuracy may be reduced.
            </div>""",
            unsafe_allow_html=True,
        )

    # ── Input mode selector ──────────────────────────────────────────
    st.markdown("<p class='section-header'>Input Method</p>", unsafe_allow_html=True)
    input_mode = st.radio(
        "Choose input method",
        ["🎚️  Sliders", "🔢  Number Fields"],
        horizontal=True,
        label_visibility="collapsed",
    )

    # ── Sensor input section ─────────────────────────────────────────
    st.markdown("<p class='section-header'>Back Sensor (Lower Back)</p>", unsafe_allow_html=True)
    st.markdown(
        """<div class="info-box">
        The back sensor measures trunk movement.
        <strong>X-axis</strong>: vertical (gravity direction) ·
        <strong>Y-axis</strong>: side-to-side ·
        <strong>Z-axis</strong>: forward/backward.
        Typical values range from <strong>−2g to +2g</strong>.
        </div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    use_sliders = "Slider" in input_mode

    with col1:
        if use_sliders:
            back_x = st.slider("back_x  (vertical)", -4.0, 4.0, 0.0, 0.00001, format="%.5f",  key="bx")
        else:
            back_x = st.number_input("back_x  (vertical)", -4.0, 4.0, 0.0, step=0.000001, format="%.6f", key="bx_n")

    with col2:
        if use_sliders:
            back_y = st.slider("back_y  (side-to-side)", -4.0, 4.0, 0.0, 0.00001, format="%.5f",  key="by")
        else:
            back_y = st.number_input("back_y  (side-to-side)", -4.0, 4.0, 0.0, step=0.000001, format="%.6f", key="by_n")

    with col3:
        if use_sliders:
            back_z = st.slider("back_z  (fwd/back)", -4.0, 4.0, 1.0, 0.00001, format="%.5f",  key="bz")
        else:
            back_z = st.number_input("back_z  (fwd/back)", -4.0, 4.0, 1.0, step=0.000001, format="%.6f", key="bz_n")

    st.markdown("<p class='section-header'>Thigh Sensor (Right Front Thigh)</p>", unsafe_allow_html=True)
    st.markdown(
        """<div class="info-box">
        The thigh sensor captures leg angle and lift.
        Its readings change dramatically between sitting (horizontal) and standing (vertical),
        making it critical for activity discrimination.
        </div>""",
        unsafe_allow_html=True,
    )

    col4, col5, col6 = st.columns(3)

    with col4:
        if use_sliders:
            thigh_x = st.slider("thigh_x  (vertical)", -4.0, 4.0, 0.0, 0.00001, format="%.5f", key="tx")
        else:
            thigh_x = st.number_input("thigh_x  (vertical)", -4.0, 4.0, 0.0, step=0.000001, format="%.6f", key="tx_n")

    with col5:
        if use_sliders:
            thigh_y = st.slider("thigh_y  (side-to-side)", -4.0, 4.0, 0.0, 0.00001, format="%.5f",  key="ty")
        else:
            thigh_y = st.number_input("thigh_y  (side-to-side)", -4.0, 4.0, 0.0, step=0.000001, format="%.6f", key="ty_n")

    with col6:
        if use_sliders:
            thigh_z = st.slider("thigh_z  (fwd/back)", -4.0, 4.0, 1.0, 0.00001, format="%.5f",  key="tz")
        else:
            thigh_z = st.number_input("thigh_z  (fwd/back)", -4.0, 4.0, 1.0, step=0.000001, format="%.6f", key="tz_n")

    # ── Quick preset buttons ─────────────────────────────────────────
    st.markdown("<p class='section-header'>Quick Presets</p>", unsafe_allow_html=True)
    st.markdown(
        """<div class="info-box">
        Load approximate sensor values for a known activity to see how the model responds.
        These are representative mean values, not exact recordings.
        </div>""",
        unsafe_allow_html=True,
    )

    preset_cols = st.columns(7)
    presets = {
        "🚶 Walking":    dict(back_x=0.1,  back_y=0.3,  back_z=0.9,  thigh_x=0.2,  thigh_y=0.1,  thigh_z=0.95),
        "🐢 Shuffling":  dict(back_x=0.05, back_y=0.1,  back_z=0.95, thigh_x=0.1,  thigh_y=0.05, thigh_z=0.98),
        "⬆️ Stairs Up":  dict(back_x=0.3,  back_y=0.1,  back_z=0.85, thigh_x=0.5,  thigh_y=0.15, thigh_z=0.80),
        "⬇️ Stairs Dn":  dict(back_x=0.25, back_y=0.1,  back_z=0.88, thigh_x=0.45, thigh_y=0.15, thigh_z=0.82),
        "🧍 Standing":   dict(back_x=0.0,  back_y=0.0,  back_z=1.0,  thigh_x=0.0,  thigh_y=0.0,  thigh_z=1.0),
        "🪑 Sitting":    dict(back_x=0.9,  back_y=0.0,  back_z=0.2,  thigh_x=0.95, thigh_y=0.0,  thigh_z=0.15),
        "🛌 Lying":      dict(back_x=0.0,  back_y=1.0,  back_z=0.05, thigh_x=0.0,  thigh_y=1.0,  thigh_z=0.05),
    }

    for col_widget, (label, vals) in zip(preset_cols, presets.items()):
        with col_widget:
            if st.button(label, key=f"preset_{label}", use_container_width=True):
                st.session_state["preset_vals"] = vals
                st.rerun()

    # Apply preset if one was just selected
    if "preset_vals" in st.session_state:
        pv = st.session_state["preset_vals"]
        back_x  = pv["back_x"]
        back_y  = pv["back_y"]
        back_z  = pv["back_z"]
        thigh_x = pv["thigh_x"]
        thigh_y = pv["thigh_y"]
        thigh_z = pv["thigh_z"]
        del st.session_state["preset_vals"]

    # ── Predict button ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, _ = st.columns([2, 5])
    with btn_col:
        predict_clicked = st.button("⚡  PREDICT ACTIVITY", use_container_width=True)

    if predict_clicked:
        sensor_values = dict(
            back_x=back_x, back_y=back_y, back_z=back_z,
            thigh_x=thigh_x, thigh_y=thigh_y, thigh_z=thigh_z,
        )

        with st.spinner("Running inference..."):
            features = extract_features_from_single_input(sensor_values)
            result   = run_prediction(features, model_name)

        if result is None:
            st.markdown(
                f"""<div class="error-box">
                    <strong>Model not loaded.</strong> Make sure
                    <code>models/{'random_forest' if 'Forest' in model_name else 'svm_linear'}.pkl</code>
                    exists in the project directory.
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            # ── Result display ───────────────────────────────────────
            st.markdown("<p class='section-header'>Prediction Result</p>", unsafe_allow_html=True)
            render_result_banner(result)

            tab1, tab2 = st.tabs(["📊  Probability Chart", "🔍  Feature Debug"])

            with tab1:
                render_probability_chart(result)

            with tab2:
                st.markdown(
                    """<div class="info-box">
                    The values below show the 60 extracted features computed from your
                    input (repeated 100× to form a 2-second window). These are the exact
                    values passed to the model after scaling.
                    </div>""",
                    unsafe_allow_html=True,
                )
                import pandas as pd
                from utils.feature_extractor import FEATURE_NAMES
                feat_df = pd.DataFrame(features, columns=FEATURE_NAMES)
                st.dataframe(feat_df.T.rename(columns={0: "Value"}).style.format("{:.5f}"),
                             use_container_width=True)
