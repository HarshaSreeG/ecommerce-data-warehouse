"""Shared utilities: logging, timing, config helpers."""

import time
import functools
from loguru import logger
import sys

# Configure loguru
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}")
logger.add("logs/etl.log", rotation="10 MB", retention="7 days", level="DEBUG")


def timer(fn):
    """Decorator: log how long a function takes."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{fn.__name__} completed in {elapsed:.2f}s")
        return result
    return wrapper


def log_step(step_name: str):
    """Context manager-style log for ETL steps."""
    logger.info(f"▶ Starting: {step_name}")
    return step_name
