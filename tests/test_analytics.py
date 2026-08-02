"""
Unit tests for TrafficAnalytics engine module.
"""

import pytest
from scripts.analytics import TrafficAnalytics

def test_analytics_calculation():
    analytics = TrafficAnalytics()
    
    # Mock tracking output with 3 cars and 1 truck
    dummy_tracking = {
        "frame_id": 1,
        "tracks": [
            {"class": "car", "bbox": [100, 100, 200, 200]},
            {"class": "car", "bbox": [250, 100, 350, 200]},
            {"class": "car", "bbox": [400, 100, 500, 200]},
            {"class": "truck", "bbox": [100, 300, 300, 500]}
        ],
        "total_unique_count": 4,
        "directions": {"North -> South": 2, "South -> North": 1}
    }

    result = analytics.analyze_frame(dummy_tracking, frame_width=1920, frame_height=1080)
    
    assert result["vehicles"] == 4
    assert result["class_distribution"]["car"] == 3
    assert result["class_distribution"]["truck"] == 1
    assert result["density"] in ["Free Flow", "Moderate Traffic", "Heavy Traffic", "Severe Congestion"]
    assert 0 <= result["congestion_score"] <= 100
    assert result["signal_optimization"]["recommended_green_sec"] >= 15
    assert "CO2" in result["emissions_g_per_min"]
    assert "recommendation" in result["route_optimization"]
