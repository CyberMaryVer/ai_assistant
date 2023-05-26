import asyncpg
from fastapi import Depends, APIRouter, Header
from loguru import logger
from typing import Union
from starlette import status

from ...core.db import get_db
from .schemas import Filter, FilterCreate, FilterInCreate, FilterUpdate, FilterOut
from .servies import filter_servise as servise
from ..companies.schemas import Company
from ...utils.auth import get_current_active_company

router = APIRouter()


@router.get("")
async def get_filters(active_only: Union[bool, None] = False,
                      company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> list[FilterOut]:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании '{company.name}'")
    logger.debug(f"{db=}")

    obj = await servise.get_many_by_company(db, company.id, active_only)

    logger.debug(f"{obj=}")

    return obj


@router.post("")
async def create_filters(obj_in: FilterInCreate,
                         user_id: str = Header(None),
                         company: Company = Depends(get_current_active_company),
                         db: asyncpg.Pool = Depends(get_db),
                         ) -> FilterOut:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании: '{company.name}'")

    filter = FilterCreate(**obj_in.dict(), company_id=company.id, created_user_id=user_id)
    obj = await servise.create(db, filter)

    logger.debug(f"{obj=}")

    return obj


@router.get("/{filter_id}")
async def get_filter(filter_id: int,
                     company: Company = Depends(get_current_active_company),
                     user_id: str = Header(None),
                     db: asyncpg.Pool = Depends(get_db),
                     ) -> FilterOut:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.get_by_company(db, filter_id, company.id)

    logger.debug(f"{obj=}")

    return obj


@router.put("/{filter_id}")
async def edit_filter(filter_id: int,
                      odj_update: FilterUpdate,
                      company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> FilterOut:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.edit_filter(db, filter_id, odj_update, company.id)

    logger.debug(f"{obj=}")
    return obj


@router.delete("/{filter_id}")
async def arhive_filter(filter_id: int,
                        company: Company = Depends(get_current_active_company),
                        user_id: str = Header(None),
                        db: asyncpg.Pool = Depends(get_db),
                        ) -> FilterOut:
    logger.info(f"[Filter] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.arhive_filter(db, filter_id, user_id, company.id)

    logger.debug(f"{obj=}")
    return obj
