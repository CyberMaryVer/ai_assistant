import asyncpg
from fastapi import FastAPI, Request
from loguru import logger
from sqlalchemy.dialects import postgresql

from fastapi_app.core.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    app.state.pool = await asyncpg.create_pool(
        str(settings.database_url),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")


async def get_db(request: Request) -> asyncpg.Pool:
        return request.app.state.pool


async def _compile(query) -> str:
    compiled_query = query.compile(dialect=postgresql.asyncpg.dialect(),
                                   compile_kwargs={"literal_binds": True}
                                   )

    logger.debug(str(compiled_query))

    return str(compiled_query)