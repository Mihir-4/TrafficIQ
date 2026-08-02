"""
TrafficIQ - System Configuration Module
Centralized configuration management for model settings, analytics parameters,
database connections, emission factors, Mistral AI integration, and output directories.
"""

import os
from pathlib import Path

# Base Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
DATABASE_DIR = BASE_DIR / "database"

# Load .env file if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                k, v = line.strip().split("=", 1)
                os.environ[k.strip()] = v.strip()

# Subdirectories in outputs
VIDEOS_OUTPUT_DIR = OUTPUTS_DIR / "videos"
REPORTS_OUTPUT_DIR = OUTPUTS_DIR / "reports"
CSV_OUTPUT_DIR = OUTPUTS_DIR / "csv"
LOGS_OUTPUT_DIR = OUTPUTS_DIR / "logs"

# Ensure all directories exist
for folder in [MODELS_DIR, OUTPUTS_DIR, DATABASE_DIR, VIDEOS_OUTPUT_DIR, REPORTS_OUTPUT_DIR, CSV_OUTPUT_DIR, LOGS_OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# AI Model Configuration
DEFAULT_MODEL_PATH = str(MODELS_DIR / "best.pt")
FALLBACK_MODEL_PATH = str(BASE_DIR / "test" / "best.pt")

CONFIDENCE_THRESHOLD = 0.25
IOU_THRESHOLD = 0.45

# Class Index Mapping for Trained YOLOv11 Model
CLASS_NAMES = {
    0: "pedestrian",
    1: "rider",
    2: "bicycle",
    3: "motorcycle",
    4: "car",
    5: "bus",
    6: "truck",
    7: "traffic light",
    8: "traffic sign",
    9: "train"
}

# Color Palette
CLASS_COLORS_RGB = {
    "pedestrian": (255, 99, 132),
    "rider": (255, 159, 64),
    "bicycle": (255, 205, 86),
    "motorcycle": (75, 192, 192),
    "car": (54, 162, 235),
    "bus": (153, 102, 255),
    "truck": (201, 203, 207),
    "traffic light": (255, 206, 86),
    "traffic sign": (46, 204, 113),
    "train": (231, 76, 60)
}

CLASS_COLORS_BGR = {
    cls: (rgb[2], rgb[1], rgb[0]) for cls, rgb in CLASS_COLORS_RGB.items()
}

# ByteTrack Tracking Parameters
TRACKER_CONFIG = "bytetrack.yaml"
TRACK_BUFFER = 30
MAX_HISTORY = 30
COUNT_LINE_POSITION = 0.5

# Analytics Engine Parameters
DENSITY_LEVELS = {
    "LOW": {"max_count": 5, "label": "Low Traffic", "color": "#2ecc71"},
    "MEDIUM": {"max_count": 15, "label": "Medium Traffic", "color": "#f1c40f"},
    "HIGH": {"max_count": 25, "label": "High Traffic", "color": "#e67e22"},
    "CONGESTED": {"max_count": 9999, "label": "Heavy Congestion", "color": "#e74c3c"}
}

# PCU Weights
PCU_WEIGHTS = {
    "car": 1.0,
    "bus": 2.2,
    "truck": 2.5,
    "motorcycle": 0.5,
    "bicycle": 0.3,
    "rider": 0.5,
    "pedestrian": 0.2,
    "train": 3.0
}

# Signal Timing Bounds (seconds)
SIGNAL_TIMING = {
    "MIN_GREEN": 15,
    "MAX_GREEN": 90,
    "DEFAULT_YELLOW": 4,
    "ALL_RED": 2,
    "BASE_CYCLE_TIME": 60
}

# Emission Rate Factors (g/min)
EMISSION_FACTORS = {
    "car": {"CO2": 21.5, "NOx": 0.12, "PM": 0.012},
    "bus": {"CO2": 65.0, "NOx": 0.95, "PM": 0.085},
    "truck": {"CO2": 58.0, "NOx": 0.82, "PM": 0.075},
    "motorcycle": {"CO2": 9.2, "NOx": 0.05, "PM": 0.005},
    "default": {"CO2": 15.0, "NOx": 0.10, "PM": 0.010}
}

# Mistral AI API Configuration (Loaded securely from environment / .env / st.secrets)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
if not MISTRAL_API_KEY:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "MISTRAL_API_KEY" in st.secrets:
            MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
    except Exception:
        pass
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"

# SQLite Database Settings
DATABASE_PATH = str(DATABASE_DIR / "traffic.db")

# Streamlit App UI Settings
APP_TITLE = "TrafficIQ - Smart Traffic Intelligence Platform"
APP_ICON = "🚦"
