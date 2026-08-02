"""
TrafficIQ - Video Processing Utilities
Encapsulates OpenCV video loading, frame iteration, metadata extraction,
and annotated video encoding/writing.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Generator, Dict, Any, Tuple, Optional
from utils.logger import setup_logger

logger = setup_logger("VideoUtils")

class VideoStreamReader:
    """Safely reads video files or camera streams frame by frame."""
    def __init__(self, source: str | int):
        self.source = source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            logger.error(f"Failed to open video source: {source}")
            raise ValueError(f"Could not open video source: {source}")

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_metadata(self) -> Dict[str, Any]:
        """Returns video metadata dict."""
        return {
            "source": str(self.source),
            "width": self.width,
            "height": self.height,
            "fps": round(self.fps, 2),
            "total_frames": self.total_frames,
            "duration_seconds": round(self.total_frames / self.fps, 2) if self.fps > 0 else 0
        }

    def frame_generator(self) -> Generator[Tuple[int, np.ndarray], None, None]:
        """Yields (frame_index, frame_image) tuples."""
        frame_idx = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret or frame is None:
                break
            frame_idx += 1
            yield frame_idx, frame

    def release(self):
        """Releases OpenCV capture object."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            logger.info(f"Video source released: {self.source}")


class VideoStreamWriter:
    """Encodes and saves processed frames to video file using OpenCV."""
    def __init__(self, output_path: str, width: int, height: int, fps: float = 30.0):
        self.output_path = output_path
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Try codecs in order of compatibility
        codecs = ['mp4v', 'avc1', 'XVID', 'MJPG']
        self.writer = None

        for codec in codecs:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if writer.isOpened():
                self.writer = writer
                logger.info(f"Initialized VideoWriter with codec '{codec}' at {output_path}")
                break

        if self.writer is None or not self.writer.isOpened():
            logger.error(f"Failed to initialize VideoWriter for {output_path}")

    def write_frame(self, frame: np.ndarray):
        """Writes a single frame to output video."""
        if self.writer and self.writer.isOpened():
            self.writer.write(frame)

    def release(self):
        """Flushes and closes VideoWriter."""
        if self.writer and self.writer.isOpened():
            self.writer.release()
            logger.info(f"VideoWriter saved: {self.output_path}")
