from typing import Generic, TypeVar, Type
from sqlalchemy.dialects import postgresql

import asyncpg
from pydantic import BaseModel

from fastapi import HTTPException, status
from sqlalchemy import select

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
            result = await connection.fetch(str(query))
            logger.debug(f"{result=}")

        companies = [Company(**r) for r in result]

        return companies


company_servise = CompanyService(models.Company)
