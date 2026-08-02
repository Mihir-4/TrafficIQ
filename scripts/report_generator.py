"""
TrafficIQ - Automated Traffic Report Generator
Generates PDF Executive Summaries, CSV frame-by-frame datasets, and Excel Workbooks
containing key traffic statistics, density breakdowns, and signal optimization reports.
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from database.database import TrafficDatabase
from configs.config import REPORTS_OUTPUT_DIR, CSV_OUTPUT_DIR
from utils.logger import setup_logger

logger = setup_logger("ReportGenerator")

class ReportGenerator:
    """Generates PDF, CSV, and Excel reports for completed traffic monitoring sessions."""
    def __init__(self, db: TrafficDatabase = None):
        self.db = db or TrafficDatabase()

    def generate_csv(self, session_id: str, output_path: str = None) -> str:
        """Generates frame-by-frame CSV export for a session."""
        frames = self.db.get_session_frames(session_id)
        if not frames:
            logger.warning(f"No frames found for session {session_id} to generate CSV.")
            return ""

        df = pd.DataFrame(frames)
        if "class_distribution_json" in df.columns:
            df.drop(columns=["class_distribution_json"], inplace=True)

        if not output_path:
            output_path = str(CSV_OUTPUT_DIR / f"{session_id}_report.csv")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Generated CSV report: {output_path}")
        return output_path

    def generate_excel(self, session_id: str, output_path: str = None) -> str:
        """Generates formatted multi-sheet Excel report for a session."""
        session_info = self.db.get_session_details(session_id)
        frames = self.db.get_session_frames(session_id)

        if not session_info or not frames:
            return ""

        if not output_path:
            output_path = str(REPORTS_OUTPUT_DIR / f"{session_id}_report.xlsx")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            # Overview Sheet
            overview_df = pd.DataFrame([session_info])
            overview_df.to_excel(writer, sheet_name="Session Overview", index=False)

            # Frame Data Sheet
            frames_df = pd.DataFrame(frames)
            if "class_distribution_json" in frames_df.columns:
                frames_df.drop(columns=["class_distribution_json"], inplace=True)
            frames_df.to_excel(writer, sheet_name="Frame Analytics", index=False)

        logger.info(f"Generated Excel report: {output_path}")
        return output_path

    def generate_pdf(self, session_id: str, output_path: str = None) -> str:
        """Generates executive PDF report using ReportLab."""
        session = self.db.get_session_details(session_id)
        frames = self.db.get_session_frames(session_id)

        if not session:
            logger.error(f"Session {session_id} not found for PDF report generation.")
            return ""

        if not output_path:
            output_path = str(REPORTS_OUTPUT_DIR / f"{session_id}_Executive_Summary.pdf")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=10
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#00ADB5"),
            spaceAfter=15
        )
        heading_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#1E293B"),
            spaceBefore=12,
            spaceAfter=6
        )

        elements = []

        # Title Header
        elements.append(Paragraph("TrafficIQ - Intelligent Traffic Analytics Report", title_style))
        elements.append(Paragraph(f"Session ID: <b>{session_id}</b> | Generated: {session.get('start_time', 'N/A')}", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#00ADB5"), spaceAfter=15))

        # Executive KPI Table
        elements.append(Paragraph("Executive Summary KPIs", heading_style))
        kpi_data = [
            ["Metric", "Value", "Metric", "Value"],
            ["Total Frames Analyzed", str(session.get("total_frames", 0)), "Total Unique Vehicles", str(session.get("total_vehicles_counted", 0))],
            ["Peak Density State", str(session.get("peak_density", "Low")), "Avg Congestion Index", f"{session.get('avg_congestion_score', 0.0):.1f} / 100"],
            ["Peak Vehicles Present", str(session.get("peak_vehicles_present", 0)), "Estimated CO2 Emissions", f"{session.get('total_co2_g', 0.0):.1f} g"]
        ]
        kpi_table = Table(kpi_data, colWidths=[130, 130, 130, 130])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6)
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 15))

        # Recommendations & Signal Optimization
        elements.append(Paragraph("Intelligent Signal Timing & Management Recommendations", heading_style))
        avg_cong = session.get('avg_congestion_score', 0.0)
        rec_text = "Traffic flow is smooth. Maintain standard 30s green light cycle."
        if avg_cong > 60:
            rec_text = "HIGH CONGESTION DETECTED: Increase main artery green light duration to 75-90s. Implement heavy vehicle lane restrictions."
        elif avg_cong > 35:
            rec_text = "MODERATE TRAFFIC: Adjust green split to 45-60s during peak traffic flow direction."

        elements.append(Paragraph(f"• <b>Recommended Traffic Controller Action:</b> {rec_text}", styles["Normal"]))
        elements.append(Spacer(1, 15))

        # Frame Analytics Sample Table
        if frames:
            elements.append(Paragraph("Sample Frame Analytics Log", heading_style))
            sample_frames = frames[:10]  # First 10 frames
            table_data = [["Frame #", "Vehicles", "Density", "Congestion Score", "Rec. Green (s)"]]
            for f in sample_frames:
                table_data.append([
                    str(f.get("frame_id", 0)),
                    str(f.get("vehicles_present", 0)),
                    str(f.get("density", "Low")),
                    f"{f.get('congestion_score', 0.0):.1f}",
                    f"{f.get('signal_timing', 30)}s"
                ])

            sample_table = Table(table_data, colWidths=[80, 100, 110, 110, 120])
            sample_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F1F5F9")]),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5)
            ]))
            elements.append(sample_table)

        doc.build(elements)
        logger.info(f"Generated PDF Executive Summary: {output_path}")
        return output_path
