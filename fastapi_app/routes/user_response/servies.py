import datetime

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, update

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from .schemas import UserResponse, UserResponseCreate, FeedbackCreate, Feedback
from ...sql_tools.models import engine


class UserResponseService:
    def __init__(self, model: models.Responses):
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

        objs = [UserResponse(**r) for r in result]

        return objs

    async def _fetchrow(self, db, query):
        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetchrow(compiled_query)

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        obj = UserResponse(**result)

        return obj

    async def get_by_company(self, db: asyncpg.Pool, _id: int, company_id: int) -> UserResponse:
        query = select(self.model).join(models.Requests,
                                        self.model.request_id == models.Requests.id
                                        ).where(self.model.id == _id).where(models.Requests.company_id == company_id)

        filter = await self._fetchrow(db, query)

        return filter

    async def get_by_request_and_company(self, db: asyncpg.Pool, request_id: int, company_id: int) -> UserResponse:
        query = select(self.model).join(models.Requests,
                                        self.model.request_id == models.Requests.id
                                        ).where(self.model.request_id == request_id).where(
            models.Requests.company_id == company_id)

        filter = await self._fetchrow(db, query)

        return filter

    async def get_query_clarifys(self, db: asyncpg.Pool, _id: int) -> list[UserResponse]:
        query = select(self.model).where(self.model.parent_id == _id)

        clarifys = await self._fetch(db, query)

        return clarifys

    async def get_clarifys(self, db: asyncpg.Pool, _id: int) -> list[UserResponse]:
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

    async def get_by_company_clarify(self, db: asyncpg.Pool, _id: int, company_id: int) -> UserResponse:
        query = select(self.model).where(self.model.id == _id).where(self.model.company_id == company_id)

        perent = await self._fetchrow(db, query)
        perent = UserResponse(**perent.dict())

        clarifys = await self.get_clarifys(db, perent.id)
        logger.warning(f"{clarifys=}")

        perent.clarify = clarifys

        return perent

    async def create(self, db: asyncpg.Pool, obj_in: UserResponseCreate) -> UserResponse:
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

    async def save(self, db: asyncpg.Pool, obj_in: UserResponseCreate) -> UserResponse:
        logger.debug(f"[save] {obj_in=}")
        query = insert(self.model).values(**obj_in.dict()).returning(self.model)

        filter = await self._fetchrow(db, query)

        return filter

    async def save_feedback(self, db: asyncpg.Pool, obj_in: FeedbackCreate, company_id: int, ) -> Feedback:
        response = await self.get_by_company(db, obj_in.respons_id, company_id)
        if not response:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        feedback = insert(models.Feedbacks).values(**obj_in.dict()).returning(models.Feedbacks)

        feedback = await self._fetchrow(db, feedback)

        return feedback


user_response_servise = UserResponseService(models.Responses)
