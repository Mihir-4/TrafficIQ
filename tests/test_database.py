"""
Unit tests for SQLite Database module.
"""

import pytest
import os
from database.database import TrafficDatabase

def test_database_crud(tmp_path):
    test_db_file = str(tmp_path / "test_traffic.db")
    db = TrafficDatabase(db_path=test_db_file)
    
    # Test session creation
    session_id = "Session_Test_001"
    assert db.create_session(session_id, source_name="test_video.mp4") is True
    
    # Test frame logging
    analytics_data = {
        "vehicles": 12,
        "class_distribution": {"car": 10, "bus": 2},
        "density": "Medium",
        "congestion_score": 42.5,
        "occupancy_ratio": 0.22,
        "signal_timing": 45,
        "emissions_g_per_min": {"CO2": 280.0}
    }
    assert db.log_frame_metric(session_id, frame_id=1, analytics=analytics_data) is True
    
    # Test session completion
    assert db.complete_session(
        session_id=session_id,
        total_frames=100,
        total_vehicles_counted=25,
        peak_density="High",
        avg_congestion=45.0,
        peak_vehicles=18,
        total_co2=1500.0
    ) is True

    # Test retrieval
    session = db.get_session_details(session_id)
    assert session is not None
    assert session["session_id"] == session_id
    assert session["total_vehicles_counted"] == 25

    frames = db.get_session_frames(session_id)
    assert len(frames) == 1
    assert frames[0]["vehicles_present"] == 12
