import logging
import sys
from loguru import logger
from fastapi_app.core.logging import InterceptHandler


def setup_logging():
    logger.remove() # remove default handler from loguru

    logger.add(sys.stderr, format="{time} {level} {message}", level="INFO", colorize=True)
    logger.add("/app/logs/debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")
    logger.add("/app/logs/info.log", format="{time} {level} {message}", level="INFO", rotation="10 MB", compression="zip")
    logger.add("/app/logs/warning.log", format="{time} {level} {message}", level="WARNING", rotation="10 MB", compression="zip")
    logger.add("/app/logs/error.log", format="{time} {level} {message}", level="ERROR", rotation="10 MB", compression="zip")
    logger.add("/app/logs/critical.log", format="{time} {level} {message}", level="CRITICAL", rotation="10 MB", compression="zip")
    logger.add("/app/logs/trace.log", format="{time} {level} {message}", level="TRACE", rotation="10 MB", compression="zip")

    return logger