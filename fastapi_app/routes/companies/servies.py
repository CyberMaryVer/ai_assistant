from typing import Generic, TypeVar, Type

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, delete

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from .schemas import CompanyUpdate, CompanyCreate, Company
from ..keys.schemas import Key
from ...sql_tools.models import engine


class CompanyService:
    def __init__(self, model: models.Company):
        self.model = model

    async def get(self, db: asyncpg.Pool, _id: int) -> list[models.Company]:
        query = select(self.model).where(self.model.id == _id)
        logger.debug(query)

        compiled_query = query.compile(bind=engine, compile_kwargs={
            "literal_binds": True})  # , dialect=postgresql.asyncpg.dialect())
        logger.debug(compiled_query)
        logger.debug(str(compiled_query))

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetchrow(str(compiled_query))
            logger.debug(f"{result=}")

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"id {_id} not found")

        company = Company(**result)
        logger.debug(f"{company}")

        return company

    async def get_many(self, db: asyncpg.Pool) -> list[models.Company]:
        query = select(self.model)
        logger.debug(query)

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetch(str(query))
            logger.debug(f"{result=}")

        companies = [Company(**r) for r in result]
        logger.debug(f"{companies}")

        return companies

    async def create(self, db: asyncpg.Pool, company_data: CompanyCreate) -> models.Company:
        query = insert(self.model).values(**company_data.dict()).returning(self.model)
        query = query.compile(bind=engine, compile_kwargs={"literal_binds": True})
        logger.debug(str(query))

        async with db.acquire() as connection:
            result = await connection.fetchrow(str(query))
            logger.debug(f"{result=}")

        company = Company(**result)

        return company

    async def get_kyes(self, db: asyncpg.Pool, _id: int) -> models.Keys:
        query = select(models.Keys).where(models.Keys.company_id == _id)
        query = query.compile(bind=engine, compile_kwargs={"literal_binds": True})
        logger.debug(str(query))

        async with db.acquire() as connection:
            result = await connection.fetch(str(query))
            logger.debug(f"{result=}")

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"id {_id} not found")

        keys = [Key(**r) for r in result]

        return keys

    async def delete_company(self, db: asyncpg.Pool, _id: int):
        query = delete(self.model).where(self.model.id == _id).returning()
        query = query.compile(bind=engine, compile_kwargs={"literal_binds": True})
        logger.debug(str(query))

        async with db.acquire() as connection:
            result = await connection.execute(str(query))
            logger.debug(f"{result=}")

        return result


company_servise = CompanyService(models.Company)
