"""
config.py — Central configuration for Paper2Code
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs")
LOG_DIR     = os.path.join(BASE_DIR, "logs")
SAMPLE_DIR  = os.path.join(BASE_DIR, "sample_papers")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR,    exist_ok=True)

# ── Flask ─────────────────────────────────────────────────────
FLASK_HOST  = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT  = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"

# ── MLflow ────────────────────────────────────────────────────
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
MLFLOW_EXPERIMENT   = os.getenv("MLFLOW_EXPERIMENT", "paper2code")

# ── Code Generation Defaults ──────────────────────────────────
DEFAULT_FRAMEWORK   = "pytorch"   # pytorch | tensorflow
DEFAULT_EPOCHS      = 10
DEFAULT_BATCH_SIZE  = 32
DEFAULT_LR          = 0.001
DEFAULT_OPTIMIZER   = "Adam"
DEFAULT_LOSS        = "CrossEntropyLoss"

# ── Supported frameworks ──────────────────────────────────────
SUPPORTED_FRAMEWORKS = ["pytorch", "tensorflow"]
