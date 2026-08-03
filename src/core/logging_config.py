from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)-15s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured = False


def configure_logging() -> None:
    """Configure HealthFlow logging once."""

    global _configured

    if _configured:
        return

    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT,
    )

    categories = {
        "application": "application.log",
        "api": "api.log",
        "quality": "quality.log",
        "pipeline": "pipeline.log",
        "frontend": "frontend.log",
    }

    for logger_name, filename in categories.items():

        logger = logging.getLogger(
            f"healthflow.{logger_name}"
        )

        logger.setLevel(logging.INFO)

        logger.propagate = False

        handler = RotatingFileHandler(
            LOG_DIRECTORY / filename,
            maxBytes=1_000_000,
            backupCount=5,
            encoding="utf-8",
        )

        handler.setFormatter(formatter)

        logger.handlers.clear()

        logger.addHandler(handler)

    _configured = True


def get_logger(
    category: str,
) -> logging.Logger:
    """Return a configured HealthFlow logger."""

    configure_logging()

    return logging.getLogger(
        f"healthflow.{category}"
    )