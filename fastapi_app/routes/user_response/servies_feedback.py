import datetime

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, update

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from fastapi_app.sql_tools.models import engine
from .schemas import FeedbackCreate, Feedback
from .servies import user_response_servise


class FeedbackService:
    def __init__(self, model: models.Feedbacks):
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

        objs = [Feedback(**r) for r in result]

        return objs

    async def _fetchrow(self, db, query):
        compiled_query = await self._compile(query)

        async with db.acquire() as connection:
            result = await connection.fetchrow(compiled_query)

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        obj = Feedback(**result)

        return obj


    async def get_by_company(self, db: asyncpg.Pool, _id: int, company_id: int) -> list[Feedback]:
        query = select(self.model).join(models.Responses, self.model.respons_id == models.Responses.id).join(models.Requests,
                                        models.Responses.request_id == models.Requests.id
                                        ).where(models.Responses.id == _id).where(models.Requests.company_id == company_id)
        logger.debug(query)

        feedbacks = await self._fetch(db, query)

        return feedbacks


    async def save(self, db: asyncpg.Pool, obj_in: FeedbackCreate, company_id: int, ) -> Feedback:
        response = await user_response_servise.get_by_company(db, obj_in.respons_id, company_id)
        if not response:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        feedback = insert(self.model).values(**obj_in.dict()).returning(self.model)

        feedback = await self._fetchrow(db, feedback)

        return feedback


feedback_servise = FeedbackService(models.Feedbacks)
