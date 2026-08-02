"""
Unit tests for ReportGenerator module (PDF, CSV, Excel generation).
"""

import pytest
from pathlib import Path
from database.database import TrafficDatabase
from scripts.report_generator import ReportGenerator

def test_report_generation(tmp_path):
    test_db_file = str(tmp_path / "report_test.db")
    db = TrafficDatabase(db_path=test_db_file)
    
    session_id = "Session_Report_001"
    db.create_session(session_id, source_name="test_video.mp4")
    db.log_frame_metric(session_id, 1, {"vehicles": 5, "density": "Low", "congestion_score": 15.0, "signal_timing": 30, "emissions_g_per_min": {"CO2": 100.0}})
    db.complete_session(session_id, 1, 5, "Low", 15.0, 5, 100.0)

    rg = ReportGenerator(db)

    # PDF test
    pdf_out = str(tmp_path / "test_report.pdf")
    res_pdf = rg.generate_pdf(session_id, output_path=pdf_out)
    assert Path(res_pdf).exists()
    assert Path(res_pdf).stat().st_size > 0

    # CSV test
    csv_out = str(tmp_path / "test_report.csv")
    res_csv = rg.generate_csv(session_id, output_path=csv_out)
    assert Path(res_csv).exists()

    # Excel test
    excel_out = str(tmp_path / "test_report.xlsx")
    res_excel = rg.generate_excel(session_id, output_path=excel_out)
    assert Path(res_excel).exists()
