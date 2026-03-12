"""
app/logger/logger.py
Centralized colored logging for Paper2Code.
Every module imports get_logger() from here.
"""

import logging
import os
from datetime import datetime
import colorlog

from config import LOG_DIR


def get_logger(name: str) -> logging.Logger:
    """
    Returns a color-coded logger that writes to:
      - Console  (colored, human-readable)
      - File     (plain text, timestamped)

    Usage:
        from app.logger.logger import get_logger
        log = get_logger(__name__)
        log.info("Processing started")
        log.error("Something went wrong")
    """
    logger = logging.getLogger(name)

    # Don't add handlers if already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Console Handler (colored) ─────────────────────────────
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_fmt = colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s]%(reset)s %(blue)s%(name)s%(reset)s → %(message)s",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "red,bg_white",
        },
    )
    console_handler.setFormatter(console_fmt)

    # ── File Handler (plain) ──────────────────────────────────
    log_file = os.path.join(
        LOG_DIR, f"paper2code_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s → %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
