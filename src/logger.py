import logging

from pathlib import Path

from logging.handlers import (
    TimedRotatingFileHandler,
)

LOG_DIR = Path("logs")

LOG_DIR.mkdir(
    exist_ok=True,
)

LOG_FILE = (
    LOG_DIR / "general.log"
)


def create_logger() -> logging.Logger:

    logger = logging.getLogger(
        "minzdrav"
    )

    logger.setLevel(
        logging.INFO
    )

    logger.propagate = False

    if logger.handlers:
        return logger

    handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(
        formatter
    )

    logger.addHandler(
        handler
    )

    return logger


logger = create_logger()
