"""
TrafficIQ - Computer Vision Drawing Utilities
Helper functions for annotating video frames with bounding boxes, track IDs,
trajectories, count lines, HUD statistics overlay, Signal Optimization, and Route Diversion badges.
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
from configs.config import CLASS_COLORS_BGR, CLASS_NAMES

def draw_bounding_boxes(
    frame: np.ndarray,
    detections: List[Dict[str, Any]],
    show_conf: bool = True,
    show_id: bool = True
) -> np.ndarray:
    """Draws bounding boxes, class labels, confidence, and track IDs on frame."""
    annotated = frame.copy()

    for det in detections:
        bbox = det.get("bbox", [0, 0, 0, 0])
        cls_name = det.get("class", "vehicle")
        conf = det.get("confidence", 0.0)
        track_id = det.get("track_id", None)

        x1, y1, x2, y2 = [int(v) for v in bbox]
        color = CLASS_COLORS_BGR.get(cls_name, (0, 255, 0))

        # Bounding box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

        # Label construction
        label_parts = [cls_name.capitalize()]
        if show_id and track_id is not None:
            label_parts.insert(0, f"#{track_id}")
        if show_conf:
            label_parts.append(f"{conf:.2f}")

        label = " | ".join(label_parts)

        # Label background box
        (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(
            annotated,
            (x1, max(0, y1 - th - baseline - 4)),
            (x1 + tw + 6, y1),
            color,
            -1
        )

        # Text label (white/black contrast)
        cv2.putText(
            annotated,
            label,
            (x1 + 3, max(th + 2, y1 - 4)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255) if sum(color) < 400 else (0, 0, 0),
            1,
            cv2.LINE_AA
        )

    return annotated


def draw_trajectories(
    frame: np.ndarray,
    track_histories: Dict[int, List[Tuple[int, int]]],
    max_pts: int = 20
) -> np.ndarray:
    """Draws movement trajectory trails for tracked vehicles."""
    annotated = frame.copy()

    for track_id, pts in track_histories.items():
        if len(pts) < 2:
            continue
        recent_pts = np.array(pts[-max_pts:], dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(annotated, [recent_pts], False, (0, 255, 255), 2, cv2.LINE_AA)

    return annotated


def draw_counting_line(
    frame: np.ndarray,
    line_y: int,
    total_count: int,
    label: str = "COUNT LINE"
) -> np.ndarray:
    """Draws a horizontal counting ROI line and counter badge."""
    annotated = frame.copy()
    h, w = frame.shape[:2]

    # Line
    cv2.line(annotated, (0, line_y), (w, line_y), (0, 165, 255), 2, cv2.LINE_AA)

    # Line Label Badge
    badge_text = f"{label}: {total_count}"
    cv2.putText(
        annotated,
        badge_text,
        (20, line_y - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 165, 255),
        2,
        cv2.LINE_AA
    )

    return annotated


def draw_hud_overlay(
    frame: np.ndarray,
    metrics: Dict[str, Any],
    fps: float = 0.0
) -> np.ndarray:
    """Draws a sleek semi-transparent HUD overlay with metrics on the top left of the frame."""
    annotated = frame.copy()
    h, w = frame.shape[:2]

    overlay_w = min(420, w - 20)
    overlay_h = 145

    # Create semi-transparent glass panel
    sub_img = annotated[10:10+overlay_h, 10:10+overlay_w]
    black_rect = np.zeros(sub_img.shape, dtype=np.uint8)
    res = cv2.addWeighted(sub_img, 0.25, black_rect, 0.75, 1.0)
    annotated[10:10+overlay_h, 10:10+overlay_w] = res

    # Border
    cv2.rectangle(annotated, (10, 10), (10 + overlay_w, 10 + overlay_h), (0, 242, 254), 1)

    # Metrics text
    veh_count = metrics.get("vehicles", 0)
    density_str = metrics.get("density", "Free Flow")
    congestion_score = metrics.get("congestion_score", 0)
    
    sig_opt = metrics.get("signal_optimization", {})
    curr_g = sig_opt.get("current_green_sec", 30)
    rec_g = sig_opt.get("recommended_green_sec", 30)
    imp_g = sig_opt.get("improvement_sec", 0)

    route_opt = metrics.get("route_optimization", {})
    route_rec = route_opt.get("recommendation", "All corridors clear")

    # Select color based on density level
    density_color = (46, 204, 113)  # Green
    if density_str in ["Moderate Traffic"]:
        density_color = (241, 196, 15)  # Yellow
    elif density_str in ["Heavy Traffic", "Severe Congestion"]:
        density_color = (231, 76, 60)  # Red

    cv2.putText(annotated, "TrafficIQ Intelligence HUD", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.putText(annotated, f"Vehicles Present: {veh_count} | FPS: {fps:.1f}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
    cv2.putText(annotated, f"Density State   : {density_str}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.45, density_color, 2)
    cv2.putText(annotated, f"Congestion Index: {congestion_score:.1f} / 100", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
    cv2.putText(annotated, f"Signal Split    : Current {curr_g}s -> Rec {rec_g}s ({'+' if imp_g>=0 else ''}{imp_g}s)", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)
    
    # Truncate route recommendation text for HUD
    short_route = route_rec if len(route_rec) < 48 else route_rec[:45] + "..."
    cv2.putText(annotated, f"Route Diversion : {short_route}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 165, 0), 1)

    return annotated
