"""
Unit tests for YOLOv11 TrafficDetector module.
"""

import pytest
import numpy as np
from scripts.detector import TrafficDetector
from configs.config import DEFAULT_MODEL_PATH

def test_detector_initialization():
    detector = TrafficDetector(model_path=DEFAULT_MODEL_PATH)
    assert detector is not None
    assert detector.model is not None
    assert len(detector.class_names) > 0

def test_detector_frame_inference():
    detector = TrafficDetector(model_path=DEFAULT_MODEL_PATH)
    # Create dummy black frame 640x640
    dummy_frame = np.zeros((640, 640, 3), dtype=np.uint8)
    output = detector.detect_frame(dummy_frame, frame_id=1)
    
    assert "frame_id" in output
    assert output["frame_id"] == 1
    assert "objects" in output
    assert isinstance(output["objects"], list)
