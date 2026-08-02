"""
TrafficIQ - Interactive Analytics Dashboard
Renders interactive Plotly charts: Vehicle Count Timeline, Vehicle Distribution Pie Chart,
Congestion Graph, Density Graph, Emission Graph, and Traffic Composition.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from database.database import TrafficDatabase
from utils.ui import apply_custom_css, render_header

st.set_page_config(page_title="TrafficIQ - Analytics Dashboard", page_icon="📊", layout="wide")

apply_custom_css()
render_header("Interactive Analytics Dashboard", "Comprehensive traffic timelines, class share pie charts, congestion curves, emissions graphs, and signal optimization reports", "📊")

db = TrafficDatabase()
db.cleanup_empty_sessions()

# Filter out empty 0-frame sessions
sessions = db.get_all_sessions(include_empty=False)

if not sessions:
    st.info("No completed session records found in database. Run a video upload session first!")
else:
    selected_sid = st.selectbox("Select Traffic Monitoring Session to Inspect", [s["session_id"] for s in sessions])

    session_info = db.get_session_details(selected_sid)
    frames = db.get_session_frames(selected_sid)

    if session_info and frames:
        st.subheader(f"Session Overview: {selected_sid}")
        
        # Responsive KPI row with custom HTML cards to avoid any text truncation
        kcol1, kcol2, kcol3, kcol4, kcol5 = st.columns(5)
        with kcol1:
            st.metric("Total Frames", f"{session_info.get('total_frames', 0):,}")
        with kcol2:
            st.metric("Vehicles Counted", f"{session_info.get('total_vehicles_counted', 0):,}")
        with kcol3:
            st.metric("Peak Density", session_info.get("peak_density", "Free Flow"))
        with kcol4:
            st.metric("Avg Congestion Index", f"{session_info.get('avg_congestion_score', 0.0):.1f} / 100")
        with kcol5:
            st.metric("Total CO2 Emissions", f"{session_info.get('total_co2_g', 0.0):.1f} g")

        df = pd.DataFrame(frames)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Interactive Analytics Charts")

        col1, col2 = st.columns(2)

        with col1:
            # 1. Vehicle Count Timeline
            fig_count = px.line(
                df,
                x="frame_id",
                y="vehicles_present",
                title="1. Vehicle Count Timeline",
                labels={"vehicles_present": "Vehicles Present", "frame_id": "Frame Index"},
                color_discrete_sequence=["#00ADB5"]
            )
            fig_count.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig_count, use_container_width=True)

            # 3. Congestion Graph
            fig_cong = px.line(
                df,
                x="frame_id",
                y="congestion_score",
                title="3. Congestion Index Timeline (0 to 100)",
                labels={"congestion_score": "Congestion Index", "frame_id": "Frame Index"},
                color_discrete_sequence=["#FF2E93"]
            )
            fig_cong.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig_cong, use_container_width=True)

            # 5. Emission Graph
            fig_co2 = px.area(
                df,
                x="frame_id",
                y="co2_emission_g",
                title="5. Vehicle CO2 Emission Rate Timeline (g/min)",
                labels={"co2_emission_g": "CO2 Emissions (g)", "frame_id": "Frame Index"},
                color_discrete_sequence=["#E74C3C"]
            )
            fig_co2.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig_co2, use_container_width=True)

        with col2:
            # 2. Vehicle Distribution Pie Chart
            class_totals = {}
            for row in frames:
                cd = row.get("class_distribution", {})
                for cls, count in cd.items():
                    class_totals[cls] = class_totals.get(cls, 0) + count

            if class_totals:
                cls_df = pd.DataFrame([{"Class": k.capitalize(), "Count": v} for k, v in class_totals.items()])
                fig_pie = px.pie(
                    cls_df,
                    names="Class",
                    values="Count",
                    title="2. Vehicle Distribution & Class Share",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Teal
                )
                fig_pie.update_layout(template="plotly_dark", height=350)
                st.plotly_chart(fig_pie, use_container_width=True)

            # 4. Density Graph
            fig_density = px.histogram(
                df,
                x="density",
                title="4. Traffic Density Classification Distribution",
                labels={"density": "Density Level"},
                color="density",
                color_discrete_map={"Free Flow": "#2ECC71", "Moderate Traffic": "#F1C40F", "Heavy Traffic": "#E67E22", "Severe Congestion": "#E74C3C"}
            )
            fig_density.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig_density, use_container_width=True)

            # 6. Traffic Composition Percentage Bar Chart
            if class_totals:
                total_cls_count = sum(class_totals.values()) or 1
                comp_df = pd.DataFrame([{"Class": k.capitalize(), "Percentage": round((v / total_cls_count) * 100, 1)} for k, v in class_totals.items()])
                fig_comp = px.bar(
                    comp_df,
                    x="Class",
                    y="Percentage",
                    title="6. Traffic Composition Percentage (%)",
                    text_auto=True,
                    color_discrete_sequence=["#4FACFE"]
                )
                fig_comp.update_layout(template="plotly_dark", height=350)
                st.plotly_chart(fig_comp, use_container_width=True)
