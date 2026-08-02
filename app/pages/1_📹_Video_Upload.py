"""
TrafficIQ - Video Processing & Analytics Interface
Uploads traffic video files (MP4, AVI, MOV, MKV), executes YOLOv11 + ByteTrack AI pipeline,
displays real-time HUD annotations, performance monitoring, direction vectors,
Signal Timing Optimization, Alternate Route Diversions, keyframes, and reports.
"""

import streamlit as st
import cv2
import tempfile
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.pipeline import TrafficPipeline
from database.database import TrafficDatabase
from utils.file_utils import create_session_folder
from utils.video_utils import VideoStreamWriter
from scripts.report_generator import ReportGenerator
from utils.ui import apply_custom_css, render_header
from configs.config import CONFIDENCE_THRESHOLD

st.set_page_config(page_title="TrafficIQ - Video Processing", page_icon="📹", layout="wide")

apply_custom_css()
render_header("Video Upload Processing Engine", "Upload traffic recordings (MP4, AVI, MOV, MKV) to run AI detection, ByteTrack tracking, direction analysis, signal optimization, and route diversion recommendations", "📹")

uploaded_file = st.file_uploader("Choose a traffic video file (.mp4, .avi, .mov, .mkv)", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.success(f"Video File Ready: **{uploaded_file.name}** ({uploaded_file.size / (1024*1024):.1f} MB)")

    st.subheader("⚡ Processing Action Center")
    start_btn = st.button("🚀 Start Video Analytics Engine", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_video, col_metrics = st.columns([7, 5])

    with col_video:
        st.subheader("📹 Live Annotated Video Feed")
        st_frame = st.empty()
        progress_bar = st.progress(0)
        st_status = st.empty()

    with col_metrics:
        st.subheader("📊 Live Traffic Intelligence")
        kcol1, kcol2 = st.columns(2)
        kpi_veh = kcol1.empty()
        kpi_count = kcol2.empty()

        kcol3, kcol4 = st.columns(2)
        kpi_density = kcol3.empty()
        kpi_cong = kcol4.empty()

        st.subheader("🚦 Signal Timing Optimization")
        scol1, scol2, scol3 = st.columns(3)
        kpi_curr_g = scol1.empty()
        kpi_rec_g = scol2.empty()
        kpi_imp_g = scol3.empty()

        st.subheader("🗺️ Traffic Routing & Alternate Route Diversion")
        kpi_route_box = st.empty()

        st.subheader("↕️ Direction Movement Analysis")
        dcol1, dcol2 = st.columns(2)
        kpi_dir_ns = dcol1.empty()
        kpi_dir_sn = dcol2.empty()

        st.subheader("🖥️ Runtime Performance Monitor")
        pcol1, pcol2, pcol3 = st.columns(3)
        kpi_fps = pcol1.empty()
        kpi_inf = pcol2.empty()
        kpi_cpu = pcol3.empty()

    if start_btn:
        db = TrafficDatabase()
        db.cleanup_empty_sessions()

        session_path, session_id = create_session_folder()
        db.create_session(session_id, source_name=uploaded_file.name)

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

        out_vid_path = str(session_path / "videos" / f"{session_id}_processed.mp4")
        writer = VideoStreamWriter(out_vid_path, width, height, fps=fps)

        pipeline = TrafficPipeline(conf=CONFIDENCE_THRESHOLD)

        frame_idx = 0
        peak_vehicles = 0
        peak_density = "Free Flow"
        congestion_scores = []
        total_co2 = 0.0
        start_time = time.time()

        st_status.info("🚀 Processing video frames... Please wait.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame_idx += 1
            annotated_frame, metrics = pipeline.process_frame(frame, frame_id=frame_idx)
            writer.write_frame(annotated_frame)

            an = metrics.get("analytics", {})
            tr = metrics.get("tracking", {})
            perf = metrics.get("performance", {})
            dirs = tr.get("directions", {})
            sig_opt = an.get("signal_optimization", {})
            route_opt = an.get("route_optimization", {})

            veh_present = an.get("vehicles", 0)
            tot_unique = tr.get("total_unique_count", 0)
            density = an.get("density", "Free Flow")
            cong_score = an.get("congestion_score", 0.0)

            peak_vehicles = max(peak_vehicles, veh_present)
            if density in ["Heavy Traffic", "Severe Congestion"]:
                peak_density = density
            congestion_scores.append(cong_score)
            total_co2 += an.get("emissions_g_per_min", {}).get("CO2", 0.0) / 60.0

            db.log_frame_metric(session_id, frame_idx, an)

            # Render Frame
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            st_frame.image(rgb_frame, channels="RGB", use_container_width=True)

            # Update Live KPIs
            kpi_veh.metric("Vehicles Present", veh_present)
            kpi_count.metric("Total Unique Counted", tot_unique)
            kpi_density.metric("Density Level", density)
            kpi_cong.metric("Congestion Index", f"{cong_score:.1f} / 100")

            # Update Signal Timing Optimization
            curr_g = sig_opt.get("current_green_sec", 30)
            rec_g = sig_opt.get("recommended_green_sec", 30)
            imp_g = sig_opt.get("improvement_sec", 0)
            kpi_curr_g.metric("Static Green", f"{curr_g}s")
            kpi_rec_g.metric("AI Rec. Green", f"{rec_g}s")
            kpi_imp_g.metric("Adjustment", f"{'+' if imp_g>=0 else ''}{imp_g}s")

            # Update Route Diversion Box
            rec_text = route_opt.get("recommendation", "All corridors clear")
            prio = route_opt.get("priority", "LOW")
            prio_color = "#2ECC71" if prio == "LOW" else ("#F1C40F" if prio == "MEDIUM" else "#E74C3C")
            
            kpi_route_box.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid {prio_color}; border-radius: 10px; padding: 12px 16px;">
                    <span style="color: {prio_color}; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;">[ {prio} PRIORITY DIVERSION ]</span><br>
                    <span style="color: #F8FAFC; font-size: 0.95rem; font-weight: 600;">{rec_text}</span>
                </div>
            """, unsafe_allow_html=True)

            # Update Directions
            kpi_dir_ns.metric("North → South", dirs.get("North -> South", 0))
            kpi_dir_sn.metric("South → North", dirs.get("South -> North", 0))

            # Update Performance Monitor
            kpi_fps.metric("Processing FPS", f"{perf.get('fps', 30.0):.1f}")
            kpi_inf.metric("Inference Time", f"{perf.get('inference_ms', 0):.1f} ms")
            kpi_cpu.metric("CPU / RAM", f"{perf.get('cpu_percent', 0)}% / {perf.get('ram_percent', 0)}%")

            # Progress Bar & Time Remaining
            progress_ratio = min(1.0, frame_idx / total_frames)
            progress_bar.progress(progress_ratio)

            elapsed_s = time.time() - start_time
            rem_s = max(0, int((elapsed_s / frame_idx) * (total_frames - frame_idx))) if frame_idx > 0 else 0
            st_status.info(f"Processing Frame {frame_idx} / {total_frames} | Est. Time Remaining: {rem_s}s")

        cap.release()
        writer.release()

        avg_cong = sum(congestion_scores) / len(congestion_scores) if congestion_scores else 0.0
        final_counted = pipeline.tracker.total_unique_count

        db.complete_session(
            session_id=session_id,
            total_frames=frame_idx,
            total_vehicles_counted=final_counted,
            peak_density=peak_density,
            avg_congestion=avg_cong,
            peak_vehicles=peak_vehicles,
            total_co2=total_co2
        )

        keyframe_paths = pipeline.save_keyframes(session_path)

        st.balloons()
        st_status.success(f"Processing Complete! Session **{session_id}** saved ({frame_idx} frames, {final_counted} vehicles).")

        # Keyframe Gallery
        if keyframe_paths:
            st.subheader("🖼️ Exported Keyframe Images (Peak Events)")
            kimg_col1, kimg_col2 = st.columns(2)
            if "highest_congestion" in keyframe_paths:
                kimg_col1.image(keyframe_paths["highest_congestion"], caption=f"Highest Congestion Keyframe ({session_id})", use_container_width=True)
            if "max_vehicles" in keyframe_paths:
                kimg_col2.image(keyframe_paths["max_vehicles"], caption=f"Max Vehicle Count Keyframe ({session_id})", use_container_width=True)

        # Report Export & Download Center
        rg = ReportGenerator(db)
        pdf_path = rg.generate_pdf(session_id)
        csv_path = rg.generate_csv(session_id)
        excel_path = rg.generate_excel(session_id)

        st.subheader("📥 Export Center (PDF, CSV, Excel, Processed Video)")
        dcol1, dcol2, dcol3, dcol4 = st.columns(4)
        with dcol1:
            if Path(pdf_path).exists():
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download PDF Report", f, file_name=f"{session_id}_Summary.pdf", mime="application/pdf", use_container_width=True)
        with dcol2:
            if Path(csv_path).exists():
                with open(csv_path, "rb") as f:
                    st.download_button("📊 Download CSV Dataset", f, file_name=f"{session_id}_Data.csv", mime="text/csv", use_container_width=True)
        with dcol3:
            if Path(excel_path).exists():
                with open(excel_path, "rb") as f:
                    st.download_button("📈 Download Excel Report", f, file_name=f"{session_id}_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with dcol4:
            if Path(out_vid_path).exists():
                with open(out_vid_path, "rb") as f:
                    st.download_button("🎬 Download Processed Video", f, file_name=f"{session_id}_Processed.mp4", mime="video/mp4", use_container_width=True)
