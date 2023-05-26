import datetime
from asyncio import sleep
from typing import Generic, TypeVar, Type

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, delete, update

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from .schemas import UserRequest, UserRequestCreate, UserRequestUpdate, UserRequestDialog
from ..content_filter.schemas import Filter
from ..content_filter.servies import filter_servise
from ...sql_tools.models import engine
from ...utils.filter_message import filter_message


class UserRequestsService:
    def __init__(self, model: models.Requests):
        self.model = model

    async def _compile(self, query) -> str:
        compiled_query = query.compile(bind=engine,
                                       compile_kwargs={"literal_binds": True}
                                       )
        logger.debug(str(compiled_query))

        return str(compiled_query)

    async def _fetch(self, db, query):
        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetch(compiled_query)

        objs = [UserRequest(**r) for r in result]

        return objs

    async def _fetchrow(self, db, query):
        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetchrow(compiled_query)

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        obj = UserRequest(**result)

        return obj

    async def get(self, db: asyncpg.Pool, _id: int) -> UserRequest:
        query = select(self.model).where(self.model.id == _id)
        filter = await self._fetchrow(db, query)
        return filter

    async def get_by_company(self, db: asyncpg.Pool, _id: int, company_id: int) -> UserRequest:
        query = select(self.model).where(self.model.id == _id).where(self.model.company_id == company_id)

        filter = await self._fetchrow(db, query)
        return filter

    async def get_query_clarifys(self, db: asyncpg.Pool, _id: int) -> list[UserRequest]:
        query = select(self.model).where(self.model.parent_id == _id)

        clarifys = await self._fetch(db, query)

        return clarifys

    async def get_clarifys(self, db: asyncpg.Pool, _id: int) -> list[UserRequest]:
        logger.warning(f"start get_clarifys")

        query = select(self.model).where(self.model.parent_id == _id)

        clarifys = await self._fetch(db, query)
        logger.debug(f"{clarifys=}")
        new_clarifys = []

        if clarifys:
            for i, clarify in enumerate(clarifys):
                logger.debug(f"{i=}, {clarify=}")
                clarify.clarify = await self.get_clarifys(db, clarify.id)
                new_clarifys.append(clarify)
                logger.success(f"{i=}, {new_clarifys=}")

            return new_clarifys

        else:
            logger.debug(f"else {clarifys=}")
            return new_clarifys

    async def get_by_company_clarify(self, db: asyncpg.Pool, _id: int, company_id: int) -> UserRequest:
        query = select(self.model).where(self.model.id == _id).where(self.model.company_id == company_id)

        perent = await self._fetchrow(db, query)
        perent = UserRequest(**perent.dict())

        clarifys = await self.get_clarifys(db, perent.id)
        logger.warning(f"{clarifys=}")

        perent.clarify = clarifys

        return perent

    async def get_many(self, db: asyncpg.Pool) -> list[UserRequest]:
        query = select(self.model)
        logger.debug(query)

        async with db.acquire() as connection:
            logger.debug(f"start connection")
            result = await connection.fetch(str(query))
            logger.debug(f"{result=}")

        companies = [UserRequest(**r) for r in result]
        logger.debug(f"{companies}")

        return companies

    async def get_many_by_company(self, db: asyncpg.Pool, company_id: int, active_only: bool = False) -> list[
        UserRequest]:
        query = select(self.model).where(self.model.company_id == company_id)

        if active_only:
            query = query.where(self.model.is_archive == False)

        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetch(compiled_query)

        companies = [UserRequest(**r) for r in result]

        return companies

    async def create(self, db: asyncpg.Pool, obj_in: UserRequestCreate) -> UserRequest:
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

    async def edit_filter(self, db: asyncpg.Pool, _id: int, odj_update: UserRequestCreate, company_id: int):
        query = update(self.model).where(self.model.id == _id,
                                         self.model.company_id == company_id,
                                         self.model.is_archive == False
                                         ).values(**odj_update.dict()).returning(self.model)

        filter = await self._fetchrow(db, query)

        return filter

    async def save(self, db: asyncpg.Pool, obj_in: UserRequestCreate) -> UserRequest:
        logger.debug(f"[save] {obj_in=}")
        query = insert(self.model).values(**obj_in.dict()).returning(self.model)

        filter = await self._fetchrow(db, query)

        return filter

    async def check_filter(self, db: asyncpg.Pool, obj_in: UserRequest) -> Filter:
        logger.debug(f"[check_filter] {obj_in=}")
        filters = await filter_servise.get_many_by_company(db, obj_in.company_id, active_only=True)

        filter_rule = await filter_message(obj_in.raw_text, filters)
        logger.debug(f"[check_filter] {filter_rule=}")

        return filter_rule

    async def update(self, db: asyncpg.Pool, _id: int, odj_update: UserRequestUpdate) -> UserRequest:
        logger.debug(f"[update request] {odj_update=}")
        query = update(self.model).where(self.model.id == _id,
                                         ).values(**odj_update.dict(exclude_defaults=True)).returning(self.model)

        user_requests = await self._fetchrow(db, query)

        return user_requests

    async def request_processing(self, db: asyncpg.Pool, obj: UserRequest) -> UserRequest:
        filter = await self.check_filter(db, obj)
        logger.info(f"[Request] {filter=}")

        obj_update = UserRequestUpdate(filter_id=filter.id if filter else None,
                                       timestamp_filter=datetime.datetime.utcnow(),
                                       status="filtered_rejected" if filter else "accepted",
                                       )

        obj = await self.update(db, obj.id, obj_update)

        if filter:
            raise HTTPException(status_code=403,
                                detail=f"Запрос id={obj.id} был заблокирован фильтром id={filter.id}, описание фильтра: {filter.description}")

        return obj


async def generate_response(db: asyncpg.Pool, obj: UserRequest):
    logger.debug(f"Начали генерировать ответ на вопрос {obj.id}")

    await sleep(30)

    bot_answer = obj.raw_text[::-1]
    logger.debug(f"Получили ответ на вопрос {obj.id}, {bot_answer=}")

    if bot_answer:
        obj_update = UserRequestUpdate(status="answered",
                                       )
        await user_requests_servise.update(db, obj.id, obj_update)


user_requests_servise = UserRequestsService(models.Requests)
