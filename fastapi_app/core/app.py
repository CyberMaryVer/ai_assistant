import logging
import os
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import PostgresDsn, SecretStr

from fastapi_app.core.logging import InterceptHandler
from fastapi_app.core.base import BaseAppSettings
from fastapi_app.core.metadata import DESCRIPTION, TAGS_METADATA, CONTACT, LICENSE
from fastapi_app.config.test_config import TEST_PG_USER, TEST_PG_PASSWORD, TEST_PG_DB_NAME, TEST_PG_HOST

pg_user = os.getenv("PG_USER") or TEST_PG_USER
pg_password = os.getenv("PG_PASSWORD") or TEST_PG_PASSWORD
pg_db_name = os.getenv("PG_DB_NAME") or TEST_PG_DB_NAME
pg_host = os.getenv("PG_HOST") or TEST_PG_HOST

print(f"HOST {pg_host.upper()}:\033[92m host was identified as [{pg_host}]\033[0m")


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "AI assistant API"
    description: str = DESCRIPTION
    version: str = "0.0.0"

    database_url: PostgresDsn = f"postgresql://{pg_user}:{pg_password}@{pg_host}:5432/{pg_db_name}"
    max_connection_count: int = 10
    min_connection_count: int = 10
    # secret_key: SecretStr = pg_password

    contact = CONTACT
    license_info = LICENSE
    openapi_tags = TAGS_METADATA

    api_prefix: str = "/api"
    admin_prefix: str = "/admin"

    # jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.DEBUG
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
            "database_url": self.database_url,

        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[
            {"sink": sys.stderr, "level": self.logging_level},
            {"sink": "/app/logs/log.log", "level": self.logging_level}
        ])
