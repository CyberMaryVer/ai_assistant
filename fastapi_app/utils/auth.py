from datetime import datetime

import asyncpg
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from loguru import logger
from sqlalchemy import select

from fastapi_app.core.db import get_db, _compile
from fastapi_app.routes.companies.schemas import Company
from fastapi_app.sql_tools import models

api_key_header = APIKeyHeader(name='X-API-Key')


async def get_company_by_token(db: asyncpg.Pool, token):
    logger.debug(f"{token=}")
    logger.debug(f"{db=}")

    query = select(models.Company).join(models.Keys).where(models.Keys.key_id == token).where(
        models.Keys.expired_at > datetime.utcnow())
    compiled_query = await _compile(query)

    async with db.acquire() as connection:
        logger.debug(f"start connection")
        result = await connection.fetchrow(compiled_query)
        logger.debug(f"{result=}")

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API ключ недействительный"
        )

    company = Company(**result)

    return company


async def get_current_company(token: str = Depends(api_key_header), db: asyncpg.Pool = Depends(get_db)):
    logger.debug(f"{token=}")

    company = await get_company_by_token(db, token)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API ключ недействительный"
        )
    return company


async def get_current_active_company(current_company: Company = Depends(get_current_company)):
    if current_company.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive Company")

    return current_company
