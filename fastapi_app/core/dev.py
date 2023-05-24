import logging
from fastapi_app.core.app import AppSettings
from pydantic import Field


class DevAppSettings(AppSettings):
    # database_url: str = Field(..., env='database_url')
    # secret_key: str = Field(..., env='secret_key')
    secret_key: str = "12345678"

    debug: bool = True

    title: str = "FastAPI endpoints (dev)"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
