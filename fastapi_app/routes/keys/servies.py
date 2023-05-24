from typing import Generic, TypeVar, Type
from sqlalchemy.dialects import postgresql

import asyncpg

from sqlalchemy import select, insert, text

from loguru import logger

from fastapi_app.sql_tools import models
from .schemas import KeyUpdate, KeyCreate, Key


class KeyService:
    def __init__(self, model: models.Keys):
        self.model = model

    async def get_many(self, db: asyncpg.Pool) -> list[models.Keys]:
        query = select(self.model)
        logger.debug(query)

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetch(str(query))
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

            # company_id = await connection.fetchval("SELECT LASTVAL()")
            # logger.debug(f"{company_id=}")

        company = Key(**result)

        return company


key_servise = KeyService(models.Keys)
