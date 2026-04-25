"""
utils/feature_extractor.py

Extracts the EXACT same 42-feature set used during model training.

This file mirrors your notebook's extract_features_from_window() function
block-for-block, name-for-name, and order-for-order.

RAW FEATURE BREAKDOWN (56 features extracted by the notebook function):
┌─────────┬──────────────────────────────────────────────────────┬───────┐
│ Block   │ Description                                          │ Count │
├─────────┼──────────────────────────────────────────────────────┼───────┤
│ Block 1 │ Per-axis stats: mean, std, range, mad, median        │  30   │
│         │ (6 axes × 5 stats)                                   │       │
│ Block 2 │ Magnitude per sensor: mag_mean, mag_std, sma, energy │   8   │
│         │ (2 sensors × 4 features)                             │       │
│ Block 3 │ Zero-Crossing Rate per axis (6 axes × 1)             │   6   │
│ Block 4 │ Inter-axis correlations per sensor (2 × 3 pairs)     │   6   │
│ Block 5 │ Entropy per axis (6 axes × 1)                        │   6   │
├─────────┼──────────────────────────────────────────────────────┼───────┤
│ TOTAL   │                                                      │  56   │
└─────────┴──────────────────────────────────────────────────────┴───────┘

REMOVED — 14 redundant columns:
    6 median columns  : *_median  (correlated with mean)
    6 range columns   : *_range   (correlated with std/mad)
    back_x_std        : overlaps with back magnitude std
    back_x_zcr        : near-zero variance across classes

FINAL OUTPUT: 56 - 14 = 42 features  ← matches scaler + model input shape
"""

import numpy as np
from scipy.stats import entropy as scipy_entropy
from scipy.stats import median_abs_deviation


# ──────────────────────────────────────────────────────────────────────────────
# Sensor column names — exact same order as SENSOR_COLS in the notebook
# ──────────────────────────────────────────────────────────────────────────────
_SENSOR_COLS = ["back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z"]

# ──────────────────────────────────────────────────────────────────────────────
# All 56 feature names in the exact order the notebook appends them.
# This MUST match the loop structure in extract_features_from_window().
# ──────────────────────────────────────────────────────────────────────────────
_ALL_56_NAMES = []

# Block 1: 6 axes × 5 stats = 30  (order: mean, std, range, mad, median)
for col in _SENSOR_COLS:
    for stat in ['mean', 'std', 'range', 'mad', 'median']:
        _ALL_56_NAMES.append(f"{col}_{stat}")

# Block 2: 2 sensors × 4 magnitude features = 8
for sensor in ['back', 'thigh']:
    for feat in ['magnitude_mean', 'magnitude_std', 'sma', 'energy']:
        _ALL_56_NAMES.append(f"{sensor}_{feat}")

# Block 3: 6 axes × 1 ZCR = 6
for col in _SENSOR_COLS:
    _ALL_56_NAMES.append(f"{col}_zcr")

# Block 4: 2 sensors × 3 correlation pairs = 6
for sensor in ['back', 'thigh']:
    for pair in ['xy_corr', 'xz_corr', 'yz_corr']:
        _ALL_56_NAMES.append(f"{sensor}_{pair}")

# Block 5: 6 axes × 1 entropy = 6
for col in _SENSOR_COLS:
    _ALL_56_NAMES.append(f"{col}_entropy")

assert len(_ALL_56_NAMES) == 56, f"Expected 56 raw feature names, got {len(_ALL_56_NAMES)}"

# ──────────────────────────────────────────────────────────────────────────────
# The 14 redundant columns removed in the training notebook
# ──────────────────────────────────────────────────────────────────────────────
_REDUNDANT_COLS = {
    # 6 median columns — highly correlated with mean
    'back_x_median',  'back_y_median',  'back_z_median',
    'thigh_x_median', 'thigh_y_median', 'thigh_z_median',
    # 6 range columns — highly correlated with std and mad
    'back_x_range',   'back_y_range',   'back_z_range',
    'thigh_x_range',  'thigh_y_range',  'thigh_z_range',
    # 2 individual columns
    'back_x_std',   # overlaps with back magnitude std
    'back_x_zcr',   # near-zero variance across activity classes
}

assert len(_REDUNDANT_COLS) == 14, f"Expected 14 redundant cols, got {len(_REDUNDANT_COLS)}"

# ──────────────────────────────────────────────────────────────────────────────
# Final 42 feature names in the correct column order.
# This is the order the scaler and models were fitted on.
# ──────────────────────────────────────────────────────────────────────────────
FEATURE_NAMES = [n for n in _ALL_56_NAMES if n not in _REDUNDANT_COLS]

assert len(FEATURE_NAMES) == 42, (
    f"Expected 42 features after removing redundant columns, got {len(FEATURE_NAMES)}.\n"
    "Update _REDUNDANT_COLS above to match your training notebook exactly."
)


# ──────────────────────────────────────────────────────────────────────────────
# Core feature computation — mirrors notebook block-for-block
# ──────────────────────────────────────────────────────────────────────────────

def _compute_all_56(window: np.ndarray) -> dict:
    """
    Compute all 56 raw features from one window, returned as a name→value dict.
    Mirrors extract_features_from_window() in the notebook exactly.

    Parameters
    ----------
    window : np.ndarray, shape (window_size, 6)
        Column order: back_x, back_y, back_z, thigh_x, thigh_y, thigh_z
    """
    result = {}

    # ── Block 1: Per-axis statistical features (6 axes × 5 = 30) ──────────────
    for axis_idx, col in enumerate(_SENSOR_COLS):
        axis_data = window[:, axis_idx]

        result[f"{col}_mean"]   = float(np.mean(axis_data))
        result[f"{col}_std"]    = float(np.std(axis_data))
        result[f"{col}_range"]  = float(np.max(axis_data) - np.min(axis_data))
        result[f"{col}_mad"]    = float(median_abs_deviation(axis_data))
        result[f"{col}_median"] = float(np.median(axis_data))

    # ── Block 2: Magnitude features per sensor (2 sensors × 4 = 8) ────────────
    back_data  = window[:, 0:3]   # back_x, back_y, back_z
    thigh_data = window[:, 3:6]   # thigh_x, thigh_y, thigh_z

    for sensor_name, sensor_data in [('back', back_data), ('thigh', thigh_data)]:
        # Euclidean magnitude: √(x² + y² + z²) computed per row
        magnitude = np.sqrt(np.sum(sensor_data ** 2, axis=1))

        result[f"{sensor_name}_magnitude_mean"] = float(np.mean(magnitude))
        result[f"{sensor_name}_magnitude_std"]  = float(np.std(magnitude))

        # SMA: mean of the sum of absolute values across axes per row
        result[f"{sensor_name}_sma"] = float(
            np.mean(np.sum(np.abs(sensor_data), axis=1))
        )

        # Energy: mean of all squared values in this sensor block
        result[f"{sensor_name}_energy"] = float(np.mean(sensor_data ** 2))

    # ── Block 3: Zero-Crossing Rate per axis (6 × 1 = 6) ──────────────────────
    for axis_idx, col in enumerate(_SENSOR_COLS):
        axis_data = window[:, axis_idx]
        # Normalised by window length — same as notebook
        zcr = float(np.sum(np.diff(np.sign(axis_data)) != 0) / len(axis_data))
        result[f"{col}_zcr"] = zcr

    # ── Block 4: Inter-axis correlations per sensor (2 × 3 = 6) ───────────────
    for sensor_name, sensor_data in [('back', back_data), ('thigh', thigh_data)]:
        x, y, z = sensor_data[:, 0], sensor_data[:, 1], sensor_data[:, 2]

        val_xy = np.corrcoef(x, y)[0, 1]
        val_xz = np.corrcoef(x, z)[0, 1]
        val_yz = np.corrcoef(y, z)[0, 1]

        result[f"{sensor_name}_xy_corr"] = 0.0 if np.isnan(val_xy) else float(val_xy)
        result[f"{sensor_name}_xz_corr"] = 0.0 if np.isnan(val_xz) else float(val_xz)
        result[f"{sensor_name}_yz_corr"] = 0.0 if np.isnan(val_yz) else float(val_yz)

    # ── Block 5: Entropy per axis (6 × 1 = 6) ─────────────────────────────────
    for axis_idx, col in enumerate(_SENSOR_COLS):
        axis_data = window[:, axis_idx]
        hist, _   = np.histogram(axis_data, bins=10, density=True)
        result[f"{col}_entropy"] = float(scipy_entropy(hist + 1e-10))

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def extract_features(window: np.ndarray) -> np.ndarray:
    """
    Extract the final 42-feature vector from one window.

    Computes all 56 raw features then drops the same 14 redundant columns
    that were removed during training — output always matches scaler input.

    Parameters
    ----------
    window : np.ndarray, shape (window_size, 6)
        Column order: back_x, back_y, back_z, thigh_x, thigh_y, thigh_z

    Returns
    -------
    np.ndarray, shape (42,) — float32
    """
    all_feats = _compute_all_56(window)
    filtered  = [all_feats[name] for name in FEATURE_NAMES]
    return np.nan_to_num(np.array(filtered, dtype=np.float32))


def extract_features_from_single_input(sensor_dict: dict) -> np.ndarray:
    """
    Build a synthetic window from manually entered single sensor values
    by repeating the row 100 times (simulates a steady-state 2-second reading).

    Parameters
    ----------
    sensor_dict : dict with keys back_x, back_y, back_z, thigh_x, thigh_y, thigh_z

    Returns
    -------
    np.ndarray, shape (1, 42) — ready for scaler.transform() then model.predict()
    """
    row = np.array([
        sensor_dict["back_x"],
        sensor_dict["back_y"],
        sensor_dict["back_z"],
        sensor_dict["thigh_x"],
        sensor_dict["thigh_y"],
        sensor_dict["thigh_z"],
    ], dtype=np.float32)

    # Tile 100 times to form one 2-second window (100 rows × 6 axes)
    window   = np.tile(row, (100, 1))
    features = extract_features(window)   # shape (42,)
    return features.reshape(1, -1)        # shape (1, 42) for model input