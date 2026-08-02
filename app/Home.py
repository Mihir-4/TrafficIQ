"""
TrafficIQ - AI-Powered Smart Traffic Intelligence Platform
Main Landing Page & Executive Dashboard Overview.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from configs.config import APP_TITLE, APP_ICON, CLASS_NAMES, CLASS_COLORS_RGB
from database.database import TrafficDatabase
from utils.ui import apply_custom_css, render_header

st.set_page_config(
    page_title="TrafficIQ - Smart Traffic Intelligence",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Glassmorphic Design System
apply_custom_css()

render_header(
    title="TrafficIQ Platform",
    subtitle="AI-Powered Smart Traffic Monitoring, Dynamic Signal Management & Environmental Analytics",
    icon="🚦"
)

# Database Data Fetching
db = TrafficDatabase()
db.cleanup_empty_sessions()
sessions = db.get_all_sessions(include_empty=False)

total_sessions = len(sessions)
total_vehicles = sum(s.get("total_vehicles_counted", 0) for s in sessions)
avg_congestion = sum(s.get("avg_congestion_score", 0.0) for s in sessions) / total_sessions if total_sessions > 0 else 0.0
total_co2 = sum(s.get("total_co2_g", 0.0) for s in sessions)

# Top Executive KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Active Monitoring Sessions</div>
            <div class="iq-kpi-val">{total_sessions}</div>
            <div class="iq-kpi-sub">Total logged sessions</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Total Vehicles Tracked</div>
            <div class="iq-kpi-val">{total_vehicles}</div>
            <div class="iq-kpi-sub">Across 10 object classes</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Avg Congestion Index</div>
            <div class="iq-kpi-val">{avg_congestion:.1f}</div>
            <div class="iq-kpi-sub">Scaled 0 to 100 Index</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Est. CO2 Emissions</div>
            <div class="iq-kpi-val">{total_co2:.1f}g</div>
            <div class="iq-kpi-sub">Environmental footprint</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Action Hub Row
st.subheader("⚡ Quick Action Hub")
hcol1, hcol2, hcol3 = st.columns(3)

with hcol1:
    if st.button("📹 Process Video Recording", use_container_width=True):
        st.switch_page("pages/1_📹_Video_Upload.py")

with hcol2:
    if st.button("📊 Analytics Dashboard", use_container_width=True):
        st.switch_page("pages/3_📊_Analytics.py")

with hcol3:
    if st.button("🤖 Consult Mistral AI", use_container_width=True):
        st.switch_page("pages/5_🤖_AI_Assistant.py")

st.markdown("<br>", unsafe_allow_html=True)

# System Information & Activity Grid
col_classes, col_recent = st.columns([5, 7])

with col_classes:
    st.subheader("🎯 10 Supported Traffic Classes")
    class_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;'>"
    for cid, cname in CLASS_NAMES.items():
        rgb = CLASS_COLORS_RGB.get(cname, (0, 173, 181))
        class_html += f"<span style='background: rgba({rgb[0]},{rgb[1]},{rgb[2]},0.2); border: 1px solid rgb({rgb[0]},{rgb[1]},{rgb[2]}); color: #FFF; padding: 8px 14px; border-radius: 20px; font-size: 0.88rem; font-weight: 600;'>{cname.capitalize()}</span>"
    class_html += "</div>"
    st.markdown(class_html, unsafe_allow_html=True)

with col_recent:
    st.subheader("📋 Recent Monitoring Activity")
    if sessions:
        df_recent = pd.DataFrame(sessions[:5])
        st.dataframe(
            df_recent[["session_id", "source_name", "start_time", "total_vehicles_counted", "peak_density", "avg_congestion_score"]],
            use_container_width=True
        )
    else:
        st.info("No completed monitoring activity recorded yet. Launch Video Upload to start!")

st.sidebar.markdown("### 🚦 TrafficIQ Platform")
st.sidebar.info("Select a page from the sidebar menu to process videos, inspect analytics, view history, or consult Mistral AI.")
