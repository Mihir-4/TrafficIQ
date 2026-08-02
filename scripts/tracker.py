"""
TrafficIQ - Vehicle Tracking, Counting & Direction Analysis Engine
Implements ByteTrack multi-object tracking for persistent ID association across frames,
trajectory history management, line-crossing vehicle counting, and direction analysis.
"""

import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple
from ultralytics import YOLO
from configs.config import DEFAULT_MODEL_PATH, FALLBACK_MODEL_PATH, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, CLASS_NAMES, TRACKER_CONFIG, MAX_HISTORY
from utils.logger import setup_logger

logger = setup_logger("Tracker")

class VehicleTracker:
    """ByteTrack vehicle tracking, counting, and directional movement module."""
    def __init__(
        self,
        model_path: str = None,
        conf: float = CONFIDENCE_THRESHOLD,
        iou: float = IOU_THRESHOLD,
        count_line_y_ratio: float = 0.5
    ):
        self.conf = conf
        self.iou = iou
        self.count_line_y_ratio = count_line_y_ratio
        self.model_path = model_path or DEFAULT_MODEL_PATH

        if not Path(self.model_path).exists():
            self.model_path = FALLBACK_MODEL_PATH

        logger.info(f"Initializing ByteTrack tracker using model at {self.model_path}")
        self.model = YOLO(self.model_path)

        # Track management state
        self.track_histories: Dict[int, List[Tuple[int, int]]] = {}
        self.crossed_ids = set()
        self.total_unique_count = 0
        self.counts_per_class: Dict[str, int] = {}
        self.directions_count = {
            "North -> South": 0,
            "South -> North": 0,
            "West -> East": 0,
            "East -> West": 0
        }
        self.class_names = self.model.names or CLASS_NAMES

    def track_frame(self, frame: np.ndarray, frame_id: int = 0) -> Dict[str, Any]:
        """Tracks objects in frame using ByteTrack.

        Returns structured dict output:
        {
            "frame_id": 125,
            "tracks": [...],
            "total_unique_count": 42,
            "class_counts": {"car": 31, "bus": 2},
            "directions": {"North -> South": 24, "South -> North": 18}
        }
        """
        if frame is None or frame.size == 0:
            return {
                "frame_id": frame_id,
                "tracks": [],
                "total_unique_count": self.total_unique_count,
                "class_counts": self.counts_per_class,
                "directions": self.directions_count
            }

        h, w = frame.shape[:2]
        line_y = int(h * self.count_line_y_ratio)

        # Run ByteTrack tracking via Ultralytics
        results = self.model.track(
            source=frame,
            persist=True,
            tracker=TRACKER_CONFIG,
            conf=self.conf,
            iou=self.iou,
            verbose=False
        )

        active_tracks = []
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy().tolist()
                cls_id = int(box.cls[0].item())
                cls_name = self.class_names.get(cls_id, str(cls_id))
                conf = float(box.conf[0].item())

                # Track ID assigned by ByteTrack
                track_id = int(box.id[0].item()) if box.id is not None else None

                x1, y1, x2, y2 = [round(v, 1) for v in xyxy]
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                track_item = {
                    "track_id": track_id,
                    "class": cls_name,
                    "class_id": cls_id,
                    "confidence": round(conf, 3),
                    "bbox": [x1, y1, x2, y2],
                    "centroid": (cx, cy)
                }
                active_tracks.append(track_item)

                # Line-crossing, direction analysis, and ID history management
                if track_id is not None:
                    if track_id not in self.track_histories:
                        self.track_histories[track_id] = []
                    self.track_histories[track_id].append((cx, cy))
                    if len(self.track_histories[track_id]) > MAX_HISTORY:
                        self.track_histories[track_id].pop(0)

                    # Line Crossing & Direction Analysis Logic
                    if track_id not in self.crossed_ids:
                        pts = self.track_histories[track_id]
                        if len(pts) >= 2:
                            prev_y = pts[-2][1]
                            curr_y = pts[-1][1]
                            first_y = pts[0][1]
                            first_x = pts[0][0]

                            if (prev_y < line_y <= curr_y) or (prev_y > line_y >= curr_y):
                                self.crossed_ids.add(track_id)
                                self.total_unique_count += 1
                                self.counts_per_class[cls_name] = self.counts_per_class.get(cls_name, 0) + 1

                                # Vector direction determination
                                dy = curr_y - first_y
                                dx = cx - first_x
                                if abs(dy) >= abs(dx):
                                    if dy > 0:
                                        self.directions_count["North -> South"] += 1
                                    else:
                                        self.directions_count["South -> North"] += 1
                                else:
                                    if dx > 0:
                                        self.directions_count["West -> East"] += 1
                                    else:
                                        self.directions_count["East -> West"] += 1

        return {
            "frame_id": frame_id,
            "tracks": active_tracks,
            "total_unique_count": self.total_unique_count,
            "class_counts": self.counts_per_class,
            "directions": self.directions_count,
            "line_y": line_y,
            "track_histories": self.track_histories
        }

    def reset(self):
        """Resets tracker state for new video session."""
        self.track_histories.clear()
        self.crossed_ids.clear()
        self.total_unique_count = 0
        self.counts_per_class.clear()
        for k in self.directions_count:
            self.directions_count[k] = 0
        logger.info("VehicleTracker state reset.")
