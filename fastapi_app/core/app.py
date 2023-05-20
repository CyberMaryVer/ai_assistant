import logging
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger
# from pydantic import PostgresDsn, SecretStr

from fastapi_app.core.logging import InterceptHandler
from fastapi_app.core.base import BaseAppSettings

LOGO = """
<! -- <img src="https://storage.googleapis.com/bubble-finder/$HR16UrfpfVQhqu2eRHDnaeTCRwSVICW1Uq0tVhSc3VbNEC7SeLSGm2"  
width="250" height="250"> -->
"""

DESCRIPTION = """
AI assistant API

АПИ для работы с AI-ассистентом. Позволяет выполнять следующие операции:

## ДЛЯ РАЗРАБОТЧИКОВ
* Регистрация пользователей
* Аутентификация пользователей
* Генерация нового ключа доступа к АПИ (при этом ключ привязан к компании и к конкретной тематике)
* Получение списка ключей доступа к АПИ для конкретной компании
* Удаление ключа доступа к АПИ

## ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
* Получение списка тематик
* Получение списка тематик, доступных для конкретного пользователя
* Получение ответа от AI-ассистента по конкретной тематике
* Получение списка ответов от AI-ассистента по конкретной тематике

"""

TAGS_METADATA = [
    {
        "name": "AI assistant API",
        "description": "Documentation for AI assistant API is available here.",
        "externalDocs": {
            "description": "External docs",
            "url": "localhost:8000/redoc",
        },
    },
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "files",
        "description": "Operations with files.",
    },
    {
        "name": "dev",
        "description": "Operations for developers. These endpoints are not available in production."
    },
    {
        "name": "healthcheck",
        "description": "Healthcheck endpoint. Returns 200 if the service is up and running.",
    },
]


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "AI assistant API"
    version: str = "0.0.0"

    # database_url: PostgresDsn
    # max_connection_count: int = 10
    # min_connection_count: int = 10
    #
    # secret_key: SecretStr
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
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])