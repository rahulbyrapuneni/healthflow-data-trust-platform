from logging.handlers import RotatingFileHandler

from src.core.logging_config import get_logger


def test_get_logger_returns_configured_logger():
    logger = get_logger("api")

    assert logger.name == "healthflow.api"
    assert logger.level > 0
    assert logger.propagate is False
    assert any(
        isinstance(handler, RotatingFileHandler)
        for handler in logger.handlers
    )


def test_quality_logger_is_configured():
    logger = get_logger("quality")

    assert logger.name == "healthflow.quality"
    assert any(
        isinstance(handler, RotatingFileHandler)
        for handler in logger.handlers
    )


def test_different_categories_use_different_loggers():
    api_logger = get_logger("api")
    pipeline_logger = get_logger("pipeline")

    assert api_logger is not pipeline_logger
    assert api_logger.name == "healthflow.api"
    assert pipeline_logger.name == "healthflow.pipeline"