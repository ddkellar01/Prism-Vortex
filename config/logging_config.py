import logging
import sys

from pythonjsonlogger import jsonlogger


def setup_logging(level: str = "INFO") -> None:
    """Configures structured JSON logging across the application."""
    logger = logging.getLogger()
    logger.setLevel(level)

    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(module)s %(message)s"
    )
    log_handler.setFormatter(formatter)

    # Clear existing handlers to prevent duplicate output
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(log_handler)


logger = logging.getLogger("prism-vortex")