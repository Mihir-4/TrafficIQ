"""
TrafficIQ - File & Workspace Utilities
Manages session directory creation, video file validation, logging directory initialization,
and structured JSON data exports.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Tuple
from configs.config import OUTPUTS_DIR, CSV_OUTPUT_DIR, REPORTS_OUTPUT_DIR, VIDEOS_OUTPUT_DIR
from utils.logger import setup_logger

logger = setup_logger("FileLogger")

def create_session_folder(base_name: str = "Session") -> Tuple[Path, str]:
    """Generates a unique session directory and returns (session_path, session_id)."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    session_id = f"{base_name}_{timestamp}"
    session_path = OUTPUTS_DIR / session_id

    session_path.mkdir(parents=True, exist_ok=True)
    (session_path / "videos").mkdir(exist_ok=True)
    (session_path / "reports").mkdir(exist_ok=True)
    (session_path / "csv").mkdir(exist_ok=True)

    logger.info(f"Created new session directory: {session_path}")
    return session_path, session_id

def validate_video_file(file_path: str) -> Tuple[bool, str]:
    """Validates if a video file exists, is non-empty, and has a supported extension."""
    path = Path(file_path)
    if not path.exists():
        return False, f"File not found: {file_path}"

    if path.stat().st_size == 0:
        return False, "File is empty (0 bytes)."

    valid_extensions = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".webm"}
    if path.suffix.lower() not in valid_extensions:
        return False, f"Unsupported format '{path.suffix}'. Supported: {', '.join(valid_extensions)}"

    return True, "Valid video file."

def save_json(data: Dict[str, Any], file_path: str) -> bool:
    """Saves dictionary data as formatted JSON."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        return False
