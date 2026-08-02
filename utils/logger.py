"""
TrafficIQ - Centralized Logging Framework
Provides logger instances writing structured log messages to console and file.
"""

import logging
import sys
from pathlib import Path
from configs.config import LOGS_OUTPUT_DIR

def setup_logger(name: str = "TrafficIQ", log_file: str = "traffic_iq.log", level=logging.INFO) -> logging.Logger:
    """Configures and returns a logger instance with console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    # Log format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    try:
        log_path = Path(LOGS_OUTPUT_DIR) / log_file
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create file logger at {log_path}: {e}")

    return logger

# Default logger instance
logger = setup_logger()
