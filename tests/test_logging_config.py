import logging

from src.core.logging_config import configure_logging


def test_logging_configuration_adds_handlers():
    logger = logging.getLogger()

    original_handlers = logger.handlers.copy()

    try:
        logger.handlers.clear()

        configure_logging()

        assert len(logger.handlers) == 2
    finally:
        logger.handlers.clear()
        logger.handlers.extend(original_handlers)