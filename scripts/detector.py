"""
TrafficIQ - YOLOv11 Object Detection Engine
Loads trained model weights (models/best.pt) and extracts structured object detection
data for traffic classes (pedestrian, rider, bicycle, motorcycle, car, bus, truck, traffic light, traffic sign, train).
"""

import os
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
from ultralytics import YOLO
from configs.config import DEFAULT_MODEL_PATH, FALLBACK_MODEL_PATH, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, CLASS_NAMES
from utils.logger import setup_logger

logger = setup_logger("Detector")

class TrafficDetector:
    """Wrapper around Ultralytics YOLOv11 model for traffic object detection."""
    def __init__(self, model_path: str = None, conf: float = CONFIDENCE_THRESHOLD, iou: float = IOU_THRESHOLD):
        self.conf = conf
        self.iou = iou
        self.model_path = model_path or DEFAULT_MODEL_PATH

        # Fallback to test/best.pt if models/best.pt not found
        if not Path(self.model_path).exists():
            if Path(FALLBACK_MODEL_PATH).exists():
                logger.warning(f"Default model not found at '{self.model_path}'. Using fallback '{FALLBACK_MODEL_PATH}'")
                self.model_path = FALLBACK_MODEL_PATH
            else:
                raise FileNotFoundError(f"YOLO model file not found at '{self.model_path}' or '{FALLBACK_MODEL_PATH}'")

        logger.info(f"Loading YOLOv11 Traffic Detection model from {self.model_path}")
        self.model = YOLO(self.model_path)
        self.class_names = self.model.names or CLASS_NAMES
        logger.info(f"YOLOv11 Detector initialized successfully with {len(self.class_names)} classes.")

    def detect_frame(self, frame: np.ndarray, frame_id: int = 0) -> Dict[str, Any]:
        """Runs YOLO object detection on a single video frame.

        Returns structured dict format:
        {
            "frame_id": 125,
            "objects": [
                {
                    "class": "car",
                    "class_id": 4,
                    "confidence": 0.92,
                    "bbox": [x1, y1, x2, y2]
                }
            ]
        }
        """
        if frame is None or frame.size == 0:
            return {"frame_id": frame_id, "objects": []}

        results = self.model.predict(
            source=frame,
            conf=self.conf,
            iou=self.iou,
            verbose=False
        )

        detected_objects = []
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            for box in boxes:
                cls_id = int(box.cls[0].item())
                cls_name = self.class_names.get(cls_id, str(cls_id))
                conf = float(box.conf[0].item())
                xyxy = box.xyxy[0].cpu().numpy().tolist()

                detected_objects.append({
                    "class": cls_name,
                    "class_id": cls_id,
                    "confidence": round(conf, 3),
                    "bbox": [round(v, 1) for v in xyxy]
                })

        return {
            "frame_id": frame_id,
            "objects": detected_objects
        }
