from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional

from loguru import logger

from fastapi_app.routes.companies.schemas import Company

api_key_header = APIKeyHeader(name='X-API-Key')




def fake_hash_password(password: str):
    return "fakehashed" + password


def decode_token(token, db: asyncpg.Pool = Depends(get_db)):
    token

    async with db.acquire() as connection:
        logger.debug(f"start connection")
        result = await connection.fetch(compiled_query)
        logger.debug(f"{result=}")

    user = get_user(users_db, token)
    return user


async def get_current_company(token: str = Depends(api_key_header)):
    logger.debug(f"{token=}")

    company = decode_token(token)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return company


async def get_current_active_company(current_company: Company = Depends(get_current_company)):
    if current_company.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive Company")
    return current_company.id
