from typing import Generic, TypeVar, Type

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, delete

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from .schemas import Filter, FilterCreate, FilterUpdate
from ..keys.schemas import Key
from ...sql_tools.models import engine


class FilterService:
    def __init__(self, model: models.Filters):
        self.model = model

    async def _compile(self, query) -> str:
        compiled_query = query.compile(bind=engine,
                                       compile_kwargs={"literal_binds": True}
                                       )
        logger.debug(str(compiled_query))

        return str(compiled_query)

    async def get(self, db: asyncpg.Pool, _id: int) -> list[Filter]:
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

        company = Filter(**result)
        logger.debug(f"{company}")

        return company

    async def get_many(self, db: asyncpg.Pool) -> list[Filter]:
        query = select(self.model)
        logger.debug(query)

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetch(str(query))
            logger.debug(f"{result=}")

        companies = [Filter(**r) for r in result]
        logger.debug(f"{companies}")

        return companies

    async def get_many_by_company(self, db: asyncpg.Pool, company_id: int, active_only: bool = False) -> list[Filter]:
        query = select(self.model).where(self.model.company_id == company_id)

        if active_only:
            query = query.where(self.model.is_archive == False)

        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetch(compiled_query)
            logger.debug(f"{result=}")

        companies = [Filter(**r) for r in result]
        logger.debug(f"{companies}")

        return companies

    async def create(self, db: asyncpg.Pool, obj_in: FilterCreate) -> Filter:
        query = insert(self.model).values(**obj_in.dict()).returning(self.model)

        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetchrow(compiled_query)
            logger.debug(f"{result=}")

        company = Filter(**result)

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


filter_servise = FilterService(models.Filters)
