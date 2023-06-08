import datetime

import asyncpg
from fastapi import Depends, APIRouter, Header, BackgroundTasks
from loguru import logger
from starlette import status

from ..user_response.schemas import UserResponse
from ..user_response.servies import user_response_servise
from ...core.db import get_db
from .schemas import UserRequestOut, UserRequestCreate, UserRequestBase, UserRequestDialog, UserRequestUpdate
from .servies import user_requests_servise as servise, generate_response
from ..companies.schemas import Company
from ...utils.auth import get_current_active_company

router = APIRouter()


@router.get("")
async def get_filters(company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> list[UserRequestOut]:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании '{company.name}'")
    logger.debug(f"{db=}")

    obj = await servise.get_many_by_company(db, company.id)

    logger.debug(f"{obj=}")

    return obj


@router.post("")
async def user_request(background_tasks: BackgroundTasks,
                       obj_in: UserRequestBase,
                       user_id: str = Header(None),
                       chat_id: str = Header(None),
                       company: Company = Depends(get_current_active_company),
                       db: asyncpg.Pool = Depends(get_db),
                       ) -> UserRequestOut:
    logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj_save = UserRequestCreate(**obj_in.dict(),
                                 company_id=company.id,
                                 user_id=user_id,
                                 chat_id=chat_id,
                                 status="received")
    obj = await servise.save(db, obj_save)

    obj = await servise.request_processing(db, obj)
    background_tasks.add_task(generate_response, db, obj)

    return obj


@router.get("/{request_id}/response")
async def get_request(request_id: int,
                      company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> UserResponse:
    """Получить ответ"""
    logger.info(f"[Response] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await user_response_servise.get_by_request_and_company(db, request_id, company.id)

    logger.debug(f"{obj=}")

    return obj


@router.get("/{request_id}/dialog")
async def get_dialog(request_id: int,
                     company: Company = Depends(get_current_active_company),
                     user_id: str = Header(None),
                     db: asyncpg.Pool = Depends(get_db),
                     ) -> UserRequestDialog:
    """Получить историю диалога"""
    logger.info(f"[Response] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.get_dialog(db, request_id, company.id)

    logger.debug(f"{obj=}")

    return obj


@router.get("/{request_id}")
async def get_request(request_id: int,
                      company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> UserRequestOut:
    """Получить цепочку вопросов"""

    logger.info(f"[Filter] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.get_by_company(db, request_id, company.id)

    logger.debug(f"{obj=}")

    return obj

# @router.post("/{response_id}/clarify")
# async def clarify_request(response_id: int,
#                           obj_in: UserRequestBase,
#                           user_id: str = Header(None),
#                           chat_id: str = Header(None),
#                           company: Company = Depends(get_current_active_company),
#                           db: asyncpg.Pool = Depends(get_db),
#                           ) -> UserRequestOut:
#     """Добавить уточнения"""
#
#     logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")
#     parent = await servise.get_by_company(db, response_id, company.id)
#
#     obj_save = UserRequestCreate(**obj_in.dict(),
#                                  parent_id=parent.id,
#                                  company_id=company.id,
#                                  user_id=user_id,
#                                  chat_id=chat_id,
#                                  status="received")
#
#     logger.debug(f"{obj_save=}")
#
#     obj = await servise.save(db, obj_save)
#
#     logger.debug(f"{obj=}")
#
#     return obj
