import asyncpg
from fastapi import Depends, APIRouter, Header
from loguru import logger
from starlette import status

from ...core.db import get_db
from .schemas import UserRequest, UserRequestCreate, UserRequestBase, UserRequestDialog
from .servies import user_requests_servise as servise
from ..companies.schemas import Company
from ...utils.auth import get_current_active_company

router = APIRouter()


@router.get("")
async def get_filters(company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> list[UserRequest]:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании '{company.name}'")
    logger.debug(f"{db=}")

    obj = await servise.get_many_by_company(db, company.id)

    logger.debug(f"{obj=}")

    return obj


@router.post("")
async def user_request(obj_in: UserRequestBase,
                       user_id: str = Header(None),
                       chat_id: str = Header(None),
                       company: Company = Depends(get_current_active_company),
                       db: asyncpg.Pool = Depends(get_db),
                       ) -> UserRequest:
    logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj_save = UserRequestCreate(**obj_in.dict(),
                                 company_id=company.id,
                                 user_id=user_id,
                                 chat_id=chat_id,
                                 status="received")

    logger.debug(f"{obj_save=}")

    obj = await servise.save(db, obj_save)
    logger.debug(f"{obj=}")

    status = await servise.check_filter(db, obj)


    return obj


@router.get("/{request_id}")
async def get_request(request_id: int,
                      company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> UserRequest:
    """Получить цепочку вопросов"""

    logger.info(f"[Filter] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.get_by_company(db, request_id, company.id)

    logger.debug(f"{obj=}")

    return obj


@router.post("/{response_id}/clarify")
async def clarify_request(response_id: int,
                          obj_in: UserRequestBase,
                          user_id: str = Header(None),
                          chat_id: str = Header(None),
                          company: Company = Depends(get_current_active_company),
                          db: asyncpg.Pool = Depends(get_db),
                          ) -> UserRequest:
    """Добавить уточнения"""

    logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")
    parent = await servise.get_by_company(db, response_id, company.id)

    obj_save = UserRequestCreate(**obj_in.dict(),
                                 parent_id=parent.id,
                                 company_id=company.id,
                                 user_id=user_id,
                                 chat_id=chat_id,
                                 status="received")

    logger.debug(f"{obj_save=}")

    obj = await servise.save(db, obj_save)

    logger.debug(f"{obj=}")

    return obj
