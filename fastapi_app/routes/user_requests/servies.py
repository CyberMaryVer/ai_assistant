import datetime
import os
from asyncio import sleep
from typing import Generic, TypeVar, Type

import asyncpg
from fastapi import HTTPException

from sqlalchemy import select, insert, delete, update

from loguru import logger
from starlette import status

from fastapi_app.sql_tools import models
from .schemas import UserRequest, UserRequestCreate, UserRequestUpdate, UserRequestDialog, UserResponseDialog
from ..api_routes import calling_assistant
from ..content_filter.schemas import Filter
from ..content_filter.servies import filter_servise
from ..user_response.schemas import UserResponseCreate
from ..user_response.servies import user_response_servise
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

    async def get_by_company(self, db: asyncpg.Pool, _id: int, company_id: int) -> models.Responses:
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

    async def get_resp_req(self, db: asyncpg.Pool, resp_id: int, company_id: int):
        bot_response = await user_response_servise.get_by_company(db, resp_id, company_id)

        user_request = await self.get_by_company(db, bot_response.request_id, company_id)
        user_request_pyd = UserRequestDialog.from_orm(user_request)

        user_request_pyd.response = UserResponseDialog.from_orm(bot_response)

        if user_request_pyd.parent_resp_id:
            resp_req = await self.get_resp_req(db, user_request_pyd.parent_resp_id, company_id)
            resp_req.response.clarify = UserRequestDialog.from_orm(user_request)

        return user_request_pyd

    async def get_all_resp_req(self, db: asyncpg.Pool, resp_id: int, company_id: int) -> UserRequestDialog:
        all_resp_req = None

        while resp_id:
            resp_req = await self.get_resp_req(db, resp_id, company_id)
            resp_req.response.clarify = all_resp_req
            all_resp_req = resp_req
            resp_id = all_resp_req.parent_resp_id

        return all_resp_req

    async def insert_request_to_end(self, resp_req: UserRequestDialog, request: UserRequestDialog):
        end_resp_req = resp_req
        while end_resp_req.response.clarify:
            end_resp_req = end_resp_req.response.clarify

        end_resp_req.response.clarify = request
        return resp_req

    async def get_dialog(self, db: asyncpg.Pool, _id: int, company_id: int, ) -> UserRequestDialog:
        user_request = await self.get_by_company(db, _id, company_id)

        print(user_request)
        if user_request.parent_resp_id:
            resp_req = await self.get_all_resp_req(db, user_request.parent_resp_id, company_id)

            resp_req = await self.insert_request_to_end(resp_req, UserRequestDialog.from_orm(user_request))

            return resp_req

        return user_request


async def generate_response(db: asyncpg.Pool, obj: UserRequest):
    logger.info(f"Начали генерировать ответ на вопрос {obj.id}")
    logger.debug(f"{obj=}")
    # await sleep(30)
    try:
        bot_answer = await calling_assistant(obj.raw_text, obj.topic)
    except Exception as err:
        logger.warning(f"[generate_clarify_response] {err=}")
        request_update = UserRequestUpdate(status="rate_limit")
        await user_requests_servise.update(db, obj.id, request_update)
        return False

    logger.success(f"Получили ответ на вопрос {obj.id}, {bot_answer=}")

    if bot_answer.get('answer'):
        response = UserResponseCreate(raw_text=bot_answer.get('answer'),
                                      sources=bot_answer.get('sources'),
                                      request_id=obj.id,
                                      status='successful'
                                      )

        await user_response_servise.save(db, response)

        request_update = UserRequestUpdate(status="answered")

        await user_requests_servise.update(db, obj.id, request_update)

    else:
        request_update = UserRequestUpdate(status="response_generation_error")
        await user_requests_servise.update(db, obj.id, request_update)


async def convert_dialog_to_promt(dialog: UserRequestDialog):
    promt = ''
    promt_first = "{question}\n Answer: {answer}\n"
    promt_template = "Question: {question}\n Answer: {answer}\n"
    promt_end = "Question: {question}\n"

    head_request = dialog
    while head_request.response is not None:
        if not promt:
            promt = promt_first.format(question=head_request.raw_text,
                                       answer=head_request.response.raw_text
                                       )
        else:
            promt += promt_template.format(question=head_request.raw_text,
                                           answer=head_request.response.raw_text
                                           )

        head_request = head_request.response.clarify

    else:
        promt += promt_end.format(question=head_request.raw_text)

    print(promt)

    return promt


async def generate_clarify_response(db: asyncpg.Pool, obj: UserRequest):
    logger.info(f"Начали генерировать ответ на вопрос {obj.id}")
    logger.debug(f"{obj=}")

    dialog = await user_requests_servise.get_dialog(db, obj.id, obj.company_id)
    promt_dialog = await convert_dialog_to_promt(dialog)

    try:
        bot_answer = await calling_assistant(promt_dialog, obj.topic)
    except Exception as err:
        logger.warning(f"[generate_clarify_response] {err=}")
        request_update = UserRequestUpdate(status="rate_limit")
        await user_requests_servise.update(db, obj.id, request_update)
        return False

    logger.success(f"Получили ответ на вопрос {obj.id}, {bot_answer=}")

    if bot_answer.get('answer'):
        response = UserResponseCreate(raw_text=bot_answer.get('answer'),
                                      sources=bot_answer.get('sources'),
                                      request_id=obj.id,
                                      status='successful'
                                      )

        await user_response_servise.save(db, response)

        request_update = UserRequestUpdate(status="answered")

        await user_requests_servise.update(db, obj.id, request_update)

    else:
        request_update = UserRequestUpdate(status="response_generation_error")
        await user_requests_servise.update(db, obj.id, request_update)


user_requests_servise = UserRequestsService(models.Requests)
