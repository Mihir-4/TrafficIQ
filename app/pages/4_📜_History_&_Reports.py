"""
TrafficIQ - Session History, Comparison & Export Center
Browse historical monitoring sessions, compare sessions side-by-side, filter records,
delete sessions, and download PDF reports, CSV datasets, Excel Workbooks, and processed videos.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from database.database import TrafficDatabase
from scripts.report_generator import ReportGenerator
from utils.ui import apply_custom_css, render_header
from configs.config import OUTPUTS_DIR

st.set_page_config(page_title="TrafficIQ - History & Export Center", page_icon="📜", layout="wide")

apply_custom_css()
render_header("Session History & Export Center", "Browse past traffic monitoring sessions, compare sessions side-by-side, and export executive reports", "📜")

db = TrafficDatabase()
rg = ReportGenerator(db)

# 1. Executive Summary & Maintenance Bar
sessions = db.get_all_sessions(include_empty=False)

kcol1, kcol2, kcol3, kcol4 = st.columns([3, 3, 3, 3])

total_s = len(sessions)
total_v = sum(s.get("total_vehicles_counted", 0) for s in sessions)
avg_c = sum(s.get("avg_congestion_score", 0.0) for s in sessions) / total_s if total_s > 0 else 0.0

with kcol1:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Total Logged Sessions</div>
            <div class="iq-kpi-val">{total_s}</div>
            <div class="iq-kpi-sub">Completed monitoring records</div>
        </div>
    """, unsafe_allow_html=True)

with kcol2:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Cumulative Vehicles</div>
            <div class="iq-kpi-val">{total_v:,}</div>
            <div class="iq-kpi-sub">Tracked across all runs</div>
        </div>
    """, unsafe_allow_html=True)

with kcol3:
    st.markdown(f"""
        <div class="iq-kpi-card">
            <div class="iq-kpi-title">Historical Congestion</div>
            <div class="iq-kpi-val">{avg_c:.1f}</div>
            <div class="iq-kpi-sub">Scaled 0 to 100 Index</div>
        </div>
    """, unsafe_allow_html=True)

with kcol4:
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    if st.button("🧹 Clean 0-Frame Logs", use_container_width=True):
        num_cleaned = db.cleanup_empty_sessions()
        st.success(f"Cleaned {num_cleaned} incomplete logs!")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if not sessions:
    st.info("No completed session records found in database. Upload a video or run live camera processing to generate analytics!")
else:
    # 2. Glassmorphic Filter & Search Hub
    st.subheader("🔍 Filter & Search Historical Logs")
    fcol1, fcol2 = st.columns([7, 5])
    with fcol1:
        search_query = st.text_input("Search Session ID or Source File Name", "", placeholder="Type session ID or video filename...")
    with fcol2:
        density_filter = st.selectbox("Filter by Density Classification", ["All", "Free Flow", "Low", "Moderate Traffic", "Medium", "High", "Heavy Traffic", "Heavy Congestion", "Severe Congestion"])

    filtered_sessions = sessions
    if search_query:
        filtered_sessions = [
            s for s in filtered_sessions
            if search_query.lower() in s["session_id"].lower() or search_query.lower() in str(s.get("source_name", "")).lower()
        ]
    if density_filter != "All":
        filtered_sessions = [s for s in filtered_sessions if str(s.get("peak_density")).lower() == density_filter.lower()]

    st.markdown(f"**Found {len(filtered_sessions)} session(s)** matching filter criteria:")
    df_sessions = pd.DataFrame(filtered_sessions)

    if not df_sessions.empty:
        # Display formatted table
        display_df = df_sessions[["session_id", "source_name", "start_time", "total_frames", "total_vehicles_counted", "peak_density", "avg_congestion_score", "status"]].copy()
        display_df.columns = ["Session ID", "Source Name", "Start Time", "Total Frames", "Vehicles Counted", "Peak Density", "Avg Congestion", "Status"]
        display_df["Avg Congestion"] = display_df["Avg Congestion"].map(lambda x: f"{x:.1f}")

        st.dataframe(display_df, use_container_width=True)

        st.markdown("---")

        # 3. Side-by-Side Session Comparator
        st.subheader("⚖️ Side-by-Side Session Comparison Engine")
        session_list = [s["session_id"] for s in filtered_sessions]
        
        if len(session_list) >= 2:
            ccol1, ccol2 = st.columns(2)
            with ccol1:
                s1_id = st.selectbox("Select Benchmark Session A", session_list, index=0)
            with ccol2:
                s2_id = st.selectbox("Select Target Session B", session_list, index=min(1, len(session_list)-1))

            s1 = db.get_session_details(s1_id)
            s2 = db.get_session_details(s2_id)

            if s1 and s2:
                comp_col1, comp_col2 = st.columns(2)

                with comp_col1:
                    st.markdown(f"### 🔵 Session A: `{s1_id}`")
                    st.metric("Source File", s1.get("source_name", "N/A"))
                    st.metric("Total Vehicles Tracked", f"{s1.get('total_vehicles_counted', 0):,}")
                    st.metric("Peak Density", s1.get("peak_density", "N/A"))
                    st.metric("Avg Congestion Index", f"{s1.get('avg_congestion_score', 0):.1f} / 100")
                    st.metric("Estimated CO2 Emissions", f"{s1.get('total_co2_g', 0):.1f} g")

                with comp_col2:
                    st.markdown(f"### 🟢 Session B: `{s2_id}`")
                    st.metric("Source File", s2.get("source_name", "N/A"))
                    
                    v_diff = s2.get('total_vehicles_counted', 0) - s1.get('total_vehicles_counted', 0)
                    st.metric("Total Vehicles Tracked", f"{s2.get('total_vehicles_counted', 0):,}", delta=f"{v_diff:+d}")
                    
                    st.metric("Peak Density", s2.get("peak_density", "N/A"))
                    
                    c_diff = s2.get('avg_congestion_score', 0) - s1.get('avg_congestion_score', 0)
                    st.metric("Avg Congestion Index", f"{s2.get('avg_congestion_score', 0):.1f} / 100", delta=f"{c_diff:+.1f}")
                    
                    co2_diff = s2.get('total_co2_g', 0) - s1.get('total_co2_g', 0)
                    st.metric("Estimated CO2 Emissions", f"{s2.get('total_co2_g', 0):.1f} g", delta=f"{co2_diff:+.1f} g")

        else:
            st.info("💡 Run or select at least two sessions to enable side-by-side comparative analysis.")

        st.markdown("---")

        # 4. Session Management & Export Center
        st.subheader("📥 Export Hub & Session Management")
        selected_sid = st.selectbox("Select Active Session for Export or Management", session_list)

        s_meta = db.get_session_details(selected_sid)
        if s_meta:
            st.markdown(f"""
                <div style='background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; padding: 14px 20px; margin-bottom: 16px;'>
                    <strong>Selected Session:</strong> <code>{selected_sid}</code> &nbsp;|&nbsp; 
                    <strong>Source:</strong> {s_meta.get('source_name')} &nbsp;|&nbsp; 
                    <strong>Vehicles:</strong> {s_meta.get('total_vehicles_counted')} &nbsp;|&nbsp; 
                    <strong>Peak Density:</strong> {s_meta.get('peak_density')}
                </div>
            """, unsafe_allow_html=True)

        rcol1, rcol2, rcol3, rcol4, rcol5 = st.columns(5)

        with rcol1:
            if st.button("📄 Generate PDF", use_container_width=True):
                pdf_path = rg.generate_pdf(selected_sid)
                if Path(pdf_path).exists():
                    with open(pdf_path, "rb") as f:
                        st.download_button("Download PDF Report", f, file_name=f"{selected_sid}_Summary.pdf", mime="application/pdf", use_container_width=True)

        with rcol2:
            if st.button("📊 Export CSV", use_container_width=True):
                csv_path = rg.generate_csv(selected_sid)
                if Path(csv_path).exists():
                    with open(csv_path, "rb") as f:
                        st.download_button("Download CSV Dataset", f, file_name=f"{selected_sid}_Frames.csv", mime="text/csv", use_container_width=True)

        with rcol3:
            if st.button("📈 Export Excel", use_container_width=True):
                excel_path = rg.generate_excel(selected_sid)
                if Path(excel_path).exists():
                    with open(excel_path, "rb") as f:
                        st.download_button("Download Excel Report", f, file_name=f"{selected_sid}_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

        with rcol4:
            vid_p = OUTPUTS_DIR / selected_sid / "videos" / f"{selected_sid}_processed.mp4"
            if vid_p.exists():
                with open(vid_p, "rb") as f:
                    st.download_button("🎬 Export Video", f, file_name=f"{selected_sid}_Processed.mp4", mime="video/mp4", use_container_width=True)
            else:
                st.info("No exported video.")

        with rcol5:
            if st.button("🗑️ Delete Session", use_container_width=True):
                db.delete_session(selected_sid)
                st.warning(f"Session '{selected_sid}' deleted successfully.")
                st.rerun()

st.sidebar.markdown("### 📜 Session History")
st.sidebar.info("Use this page to compare traffic sessions, export executive PDF/CSV reports, and manage database records.")
