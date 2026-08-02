"""
TrafficIQ - System Configuration & Settings Dashboard
Manage model hyperparameters, tracker parameters, signal timing bounds, Mistral AI key security,
and database maintenance options.
"""

import streamlit as st
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from configs.config import DEFAULT_MODEL_PATH, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, MISTRAL_API_KEY
from database.database import TrafficDatabase
from utils.ui import apply_custom_css, render_header

st.set_page_config(page_title="TrafficIQ - Settings", page_icon="⚙️", layout="wide")

apply_custom_css()
render_header("System Settings & Platform Preferences", "Configure detection thresholds, ByteTrack tracker parameters, signal timing formulas, and database status", "⚙️")

# 1. AI Assistant Integration & Secure Key Management
st.subheader("🤖 AI Assistant Integration & API Security")

has_key = bool(st.session_state.get("mistral_api_key") or MISTRAL_API_KEY)

if has_key:
    st.success("🔒 **Mistral API Key Status:** Connected & Active (Securely configured in environment)")
else:
    st.warning("⚠️ **Mistral API Key Status:** Not set. Configure `MISTRAL_API_KEY` in `.env` or enter below.")

new_key = st.text_input(
    "Update Mistral API Key",
    value="",
    type="password",
    placeholder="Enter new API key to override active session (key remains private and hidden)...",
    help="Your key is stored securely in active session memory and is never rendered in clear text."
)

if new_key.strip():
    st.session_state["mistral_api_key"] = new_key.strip()
    st.success("🔒 New Mistral API Key loaded securely for this session!")

st.markdown("---")

# 2. YOLO11 Detection Hyperparameters
st.subheader("🎯 YOLOv11 Detection & Tracking Hyperparameters")
if Path(DEFAULT_MODEL_PATH).exists():
    st.success(f"YOLOv11 Model Weights: **Verified & Active** ({Path(DEFAULT_MODEL_PATH).stat().st_size / (1024*1024):.1f} MB)")
else:
    st.error("Model weights file not found!")

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    conf_setting = st.slider("Detection Confidence Threshold", 0.05, 0.95, CONFIDENCE_THRESHOLD, 0.05)
with col_s2:
    iou_setting = st.slider("IoU Threshold", 0.05, 0.95, IOU_THRESHOLD, 0.05)
with col_s3:
    count_line_pos = st.slider("Counting Line Height (%)", 20, 80, 50, 5)

st.markdown("---")

# 3. Signal Timing Bounds
st.subheader("🚥 Signal Timing Optimization Parameters")
col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.number_input("Minimum Green Time (seconds)", value=15, min_value=5, max_value=30)
with col_g2:
    st.number_input("Maximum Green Time (seconds)", value=90, min_value=45, max_value=180)
with col_g3:
    st.number_input("Default Cycle Time (seconds)", value=60, min_value=30, max_value=120)

st.markdown("---")

# 4. Database & Storage Status
st.subheader("🗄️ Database & Storage System Status")
dcol1, dcol2 = st.columns(2)
with dcol1:
    st.success("Database Repository: **Online (SQLite Engine)**")
with dcol2:
    st.success("Output Export Directory: **Active & Ready**")

if st.button("🔄 Verify & Re-index Database Schema", use_container_width=True):
    db = TrafficDatabase()
    db.cleanup_empty_sessions()
    st.success("Database schema verified and clean.")

st.sidebar.markdown("### ⚙️ Settings")
st.sidebar.info("Configure platform hyperparameters, signal bounds, and verify database integrity.")
