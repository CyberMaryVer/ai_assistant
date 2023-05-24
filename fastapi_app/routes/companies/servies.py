from typing import Generic, TypeVar, Type
from sqlalchemy.dialects import postgresql

import asyncpg

from sqlalchemy import select, insert, text

from loguru import logger

from fastapi_app.sql_tools import models
from .schemas import CompanyUpdate, CompanyCreate, Company


class CompanyService:
    def __init__(self, model: models.Company):
        self.model = model

    async def get_many(self, db: asyncpg.Pool) -> list[models.Company]:
        query = select(self.model)
        logger.debug(query)

        async with db.acquire() as connection:
            result = await connection.fetch(query)
            logger.debug(f"{result=}")

        companies = [Company(**r) for r in result]

        return companies

    async def create(self, db: asyncpg.Pool, company_data: CompanyCreate) -> models.Company:
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

        keys = company_data.dict().keys()
        placeholders = [f"${i + 1}" for i in range(len(keys))]

        query = f"""
            INSERT INTO companies ({",".join(keys)})
            VALUES ({', '.join(placeholders)})
            RETURNING id, {",".join(keys)}
        """

        values = list(company_data.dict().values())

        logger.debug(f"{query=}")
        logger.debug(f"{values=}")

        async with db.acquire() as connection:
            result = await connection.fetchrow(query, *values)
            logger.debug(f"{result=}")

            # company_id = await connection.fetchval("SELECT LASTVAL()")
            # logger.debug(f"{company_id=}")

        company = Company(**result)

        return company


company_servise = CompanyService(models.Company)
