import logging

from fastapi_app.core.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "FastAPI endpoints (dev)"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"