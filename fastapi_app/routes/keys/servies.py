from typing import Generic, TypeVar, Type

from fastapi import HTTPException
from sqlalchemy.dialects import postgresql

import asyncpg

from sqlalchemy import select, insert, text, delete

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from .schemas import KeyUpdate, KeyCreate, Key
from ...sql_tools.models import engine


class KeyService:
    def __init__(self, model: models.Keys):
        self.model = model

    async def _compile(self, query) -> str:
        compiled_query = query.compile(bind=engine,
                                       compile_kwargs={"literal_binds": True}
                                       )
        logger.debug(str(compiled_query))

        return str(compiled_query)

    async def get(self, db: asyncpg.Pool, _id: int) -> list[models.Company]:
        query = select(self.model).where(self.model.id == _id)

        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetchrow(compiled_query)
            logger.debug(f"{result=}")

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"id {_id} not found")

        key = Key(**result)
        logger.debug(f"{key}")

        return key

    async def get_many(self, db: asyncpg.Pool) -> list[models.Keys]:
        query = select(self.model)
        compile_query = await self._compile(query)

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetch(compile_query)
            logger.debug(f"{result=}")

        companies = [Key(**r) for r in result]
        logger.debug(f"{companies}")

        return companies

    async def create(self, db: asyncpg.Pool, key_data: KeyCreate) -> models.Company:
        # query = """
        #     INSERT INTO companies (name, email, website, is_disabled)
        #     VALUES ($1, $2, $3, $4)
        # """
        #
        # values = [
        #     'Company',
        #     'company@example.com',
        #     'www.example.com',
        #     False
        # ]

        keys = key_data.dict().keys()
        placeholders = [f"${i + 1}" for i in range(len(keys))]

        query = f"""
            INSERT INTO api_keys ({",".join(keys)})
            VALUES ({', '.join(placeholders)})
            RETURNING *
        """

        values = list(key_data.dict().values())

        logger.debug(f"{query=}")
        logger.debug(f"{values=}")

        async with db.acquire() as connection:
            result = await connection.fetchrow(query, *values)
            logger.debug(f"{result=}")

        company = Key(**result)

        return company

    async def delete_key(self, db: asyncpg.Pool, _id: int):
        query = delete(self.model).where(self.model.id == _id).returning()
        query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.execute(query)
            logger.debug(f"{result=}")

        return result


key_servise = KeyService(models.Keys)
