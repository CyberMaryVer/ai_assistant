import datetime
from typing import Generic, TypeVar, Type

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, delete, update

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

    async def _fetchrow(self, db, query):
        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetchrow(compiled_query)

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        obj = Filter(**result)

        return obj

    async def get(self, db: asyncpg.Pool, _id: int) -> Filter:
        query = select(self.model).where(self.model.id == _id)
        filter = await self._fetchrow(db, query)
        return filter

    async def get_by_company(self, db: asyncpg.Pool, _id: int, company_id: int) -> Filter:
        query = select(self.model).where(self.model.id == _id).where(self.model.company_id == company_id)

        filter = await self._fetchrow(db, query)
        return filter

    async def get_many(self, db: asyncpg.Pool) -> list[Filter]:
        query = select(self.model)

        async with db.acquire() as connection:
            result = await connection.fetch(str(query))

        companies = [Filter(**r) for r in result]

        return companies

    async def get_many_by_company(self, db: asyncpg.Pool, company_id: int, active_only: bool = False) -> list[Filter]:
        query = select(self.model).where(self.model.company_id == company_id)

        if active_only:
            query = query.where(self.model.is_archive == False)

        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetch(compiled_query)

        companies = [Filter(**r) for r in result]

        return companies

    async def create(self, db: asyncpg.Pool, obj_in: FilterCreate) -> Filter:
        query = insert(self.model).values(**obj_in.dict()).returning(self.model)

        filter = await self._fetchrow(db, query)

        return filter

    async def arhive_filter(self, db: asyncpg.Pool, _id: int, user_id: str, company_id: int):
        query = update(self.model).where(self.model.id == _id,
                                         self.model.company_id == company_id,
                                         self.model.is_archive == False
                                         ).values(is_archive=True,
                                                  archive_at=datetime.datetime.utcnow(),
                                                  archive_user_id=user_id,
                                                  ).returning(self.model)

        filter = await self._fetchrow(db, query)

        return filter

    async def edit_filter(self, db: asyncpg.Pool, _id: int, odj_update: FilterUpdate, company_id: int):
        query = update(self.model).where(self.model.id == _id,
                                         self.model.company_id == company_id,
                                         self.model.is_archive == False
                                         ).values(**odj_update.dict()).returning(self.model)

        filter = await self._fetchrow(db, query)

        return filter


filter_servise = FilterService(models.Filters)
