"""
Project configuration for the reproducible IDS pipeline.

This file centralizes paths, column names, random seeds, and model
settings so that the project can be run outside the notebook.
"""

from pathlib import Path


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

RAW_CICIDS2017_DIR = RAW_DATA_DIR / "cicids2017"

# Optional original prepared source sample.
# Place the source file here if using the original repository sample.
SOURCE_SAMPLE_PATH = RAW_DATA_DIR / "cic_0.01km.csv"

# Final prepared dataset used by the reproducible scripts.
PREPARED_DATA_PATH = PROCESSED_DATA_DIR / "cicids2017_prepared_sample.csv"


# ============================================================
# Dataset constants
# ============================================================

TARGET_COLUMN = "Label"

BENIGN_VALUE = 0
ATTACK_VALUE = 1

RANDOM_SEED = 42

EXPECTED_TOTAL_ROWS = 28303
EXPECTED_BENIGN_ROWS = 22662
EXPECTED_ATTACK_ROWS = 5641

EXPECTED_FEATURE_COUNT = 19


# ============================================================
# Final predictor columns
# ============================================================

FEATURE_COLUMNS = [
    "Flow Duration",
    "Total Length of Fwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Flow IAT Mean",
    "Flow IAT Min",
    "Fwd IAT Min",
    "Fwd Header Length",
    "Bwd Header Length",
    "Fwd Packets/s",
    "Bwd Packets/s",
    "Min Packet Length",
    "URG Flag Count",
    "Down/Up Ratio",
    "Init_Win_bytes_forward",
    "Init_Win_bytes_backward",
    "min_seg_size_forward",
]

REQUIRED_COLUMNS = FEATURE_COLUMNS + [TARGET_COLUMN]


# ============================================================
# Corrected split configuration
# ============================================================

TRAIN_SIZE_APPROX = 16851
VALIDATION_SIZE_APPROX = 5785
TEST_SIZE_APPROX = 5667

TEST_SIZE = 0.20
VALIDATION_SIZE_FROM_DEVELOPMENT = 0.2555

GROUP_COLUMN = "duplicate_profile_group"


# ============================================================
# Final model configuration
# ============================================================

FINAL_MODEL_NAME = "LGBM_00_initial"
FINAL_THRESHOLD = 0.546

LIGHTGBM_PARAMS = {
    "objective": "binary",
    "random_state": RANDOM_SEED,
    "n_estimators": 300,
    "learning_rate": 0.05,
    "num_leaves": 31,
    "max_depth": -1,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
    "class_weight": None,
    "n_jobs": -1,
    "verbose": -1,
}


# ============================================================
# Output paths
# ============================================================

FINAL_METRICS_PATH = OUTPUTS_DIR / "final_metrics.csv"
FINAL_CONFUSION_MATRIX_PATH = OUTPUTS_DIR / "final_confusion_matrix.csv"


# ============================================================
# Utility
# ============================================================

def ensure_project_directories() -> None:
    """Create project folders required by the runnable scripts."""
    DATA_DIR.mkdir(exist_ok=True)
    RAW_DATA_DIR.mkdir(exist_ok=True)
    RAW_CICIDS2017_DIR.mkdir(exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)
