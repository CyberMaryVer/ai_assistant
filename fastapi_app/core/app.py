import logging
import os
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import PostgresDsn, SecretStr

from fastapi_app.core.logging import InterceptHandler
from fastapi_app.core.base import BaseAppSettings
from fastapi_app.core.metadata import DESCRIPTION, TAGS_METADATA
from fastapi_app.config.test_config import TEST_USER, TEST_KEY, TEST_DB

secret_user = TEST_USER or os.getenv("SECRET_USER")
secret_key = TEST_KEY or os.getenv("SECRET_KEY")
db_name = TEST_DB or os.getenv("DB_NAME")
host = os.getenv("HOST") or "localhost"

print(f"HOST {host.upper()}:\033[92m host was identified as [{host}]\033[0m")


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "AI assistant API"
    description: str = DESCRIPTION
    version: str = "0.0.0"

    database_url: PostgresDsn = f"postgresql://{secret_user}:{secret_key}@{host}:5432/{db_name}"
    max_connection_count: int = 10
    min_connection_count: int = 10
    secret_key: SecretStr = secret_key

    contact = {
        "name": "AI ENGINEERS",
        "url": "https://gitlab.com/maria.startseva",
        "email": "mary-ver@yandex.ru",
    }
    license_info = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
    openapi_tags = TAGS_METADATA
    servers = [
        {"url": "localhost:8000"},
        {"url": "localhost:9000", "description": "Staging environment"},
    ]

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "contact": self.contact,
            "license_info": self.license_info,
            "openapi_tags": self.openapi_tags,
            # "servers": self.servers,
            "database_url": self.database_url,
            "secret_key": self.secret_key,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
