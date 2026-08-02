"""
TrafficIQ - AI Pipeline Orchestrator
Coordinates frame loading, YOLOv11 detection, ByteTrack tracking,
direction analysis, traffic metrics calculation, visual HUD annotation,
keyframe export, and database persistence.
"""

import cv2
import time
import psutil
import torch
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from scripts.detector import TrafficDetector
from scripts.tracker import VehicleTracker
from scripts.analytics import TrafficAnalytics
from utils.drawing import draw_bounding_boxes, draw_trajectories, draw_counting_line, draw_hud_overlay
from configs.config import OUTPUTS_DIR
from utils.logger import setup_logger

logger = setup_logger("Pipeline")

class TrafficPipeline:
    """Orchestrates end-to-end computer vision and traffic intelligence processing."""
    def __init__(self, model_path: str = None, conf: float = 0.25, iou: float = 0.45):
        logger.info("Initializing TrafficIQ AI Pipeline...")
        self.tracker = VehicleTracker(model_path=model_path, conf=conf, iou=iou)
        self.analytics = TrafficAnalytics()
        self.fps_history = []
        
        # Keyframe Tracking State
        self.max_congestion_score = -1.0
        self.max_vehicle_count = -1
        self.keyframe_max_congestion: Optional[np.ndarray] = None
        self.keyframe_max_vehicles: Optional[np.ndarray] = None
        
        logger.info("TrafficIQ AI Pipeline ready.")

    def process_frame(self, frame: np.ndarray, frame_id: int = 0) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Processes a single frame through Tracking -> Direction Analysis -> Analytics -> Visual Overlay.

        Returns (annotated_frame, frame_metrics_dict).
        """
        start_time = time.time()
        if frame is None or frame.size == 0:
            return frame, {}

        h, w = frame.shape[:2]

        # Step 1: ByteTrack Multi-Object Tracking, Counting & Direction Analysis
        tracking_output = self.tracker.track_frame(frame, frame_id=frame_id)

        # Step 2: Traffic Analytics Calculation
        analytics_output = self.analytics.analyze_frame(
            tracking_output,
            frame_width=w,
            frame_height=h
        )

        # Step 3: Compute Hardware & Performance Metrics
        elapsed = time.time() - start_time
        fps = 1.0 / elapsed if elapsed > 0 else 30.0
        inference_ms = round(elapsed * 1000, 1)

        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        cuda_active = torch.cuda.is_available()

        # Step 4: Keyframe Capture Logic
        cong_score = analytics_output.get("congestion_score", 0.0)
        veh_present = analytics_output.get("vehicles", 0)

        if cong_score > self.max_congestion_score:
            self.max_congestion_score = cong_score
            self.keyframe_max_congestion = frame.copy()

        if veh_present > self.max_vehicle_count:
            self.max_vehicle_count = veh_present
            self.keyframe_max_vehicles = frame.copy()

        # Step 5: Visual Frame Annotations
        tracks = tracking_output.get("tracks", [])
        annotated = draw_bounding_boxes(frame, tracks, show_conf=True, show_id=True)
        annotated = draw_trajectories(annotated, tracking_output.get("track_histories", {}))

        line_y = tracking_output.get("line_y", int(h * 0.5))
        total_unique = tracking_output.get("total_unique_count", 0)
        annotated = draw_counting_line(annotated, line_y, total_unique, label="COUNT LINE")

        annotated = draw_hud_overlay(annotated, analytics_output, fps=fps)

        # Combined results dict
        results = {
            "frame_id": frame_id,
            "tracking": tracking_output,
            "analytics": analytics_output,
            "performance": {
                "fps": round(fps, 1),
                "inference_ms": inference_ms,
                "cpu_percent": cpu_percent,
                "ram_percent": ram_percent,
                "cuda_active": cuda_active
            },
            "line_y": line_y
        }

        return annotated, results

    def save_keyframes(self, session_path: Path) -> Dict[str, str]:
        """Saves keyframe images (Peak Congestion, Max Vehicles) to session outputs/images/ directory."""
        img_dir = session_path / "images"
        img_dir.mkdir(parents=True, exist_ok=True)
        saved_paths = {}

        if self.keyframe_max_congestion is not None:
            p1 = str(img_dir / "highest_congestion_keyframe.jpg")
            cv2.imwrite(p1, self.keyframe_max_congestion)
            saved_paths["highest_congestion"] = p1

        if self.keyframe_max_vehicles is not None:
            p2 = str(img_dir / "max_vehicles_keyframe.jpg")
            cv2.imwrite(p2, self.keyframe_max_vehicles)
            saved_paths["max_vehicles"] = p2

        logger.info(f"Saved {len(saved_paths)} keyframe images to {img_dir}")
        return saved_paths

    def reset(self):
        """Resets state for new video session."""
        self.tracker.reset()
        self.max_congestion_score = -1.0
        self.max_vehicle_count = -1
        self.keyframe_max_congestion = None
        self.keyframe_max_vehicles = None
        logger.info("Pipeline state reset for new session.")
