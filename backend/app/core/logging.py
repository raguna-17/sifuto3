import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # ----------------------
    # ensure log directory exists
    # ----------------------
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------
    # console handler
    # ----------------------
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # ----------------------
    # file handler
    # ----------------------
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console, file_handler],
    )