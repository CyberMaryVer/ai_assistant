import asyncpg
from fastapi import Depends, APIRouter
from loguru import logger
from starlette import status

from ...core.db import get_db
from .schemas import Key, KeyCreate
from .servies import key_servise as servise

router = APIRouter()


@router.get("")
async def get_keys(db: asyncpg.Pool = Depends(get_db),
                   ) -> list[Key]:
    # user_entries = get_entries_from_collection("users")
    logger.debug("endpoint /db_users/ called")
    logger.debug(f"{db=}")
    companies = await servise.get_many(db)

    logger.debug(f"{companies=}")

    return companies


@router.post("")
async def create_key(obj_in: KeyCreate,
                     db: asyncpg.Pool = Depends(get_db),
                     ) -> Key:
    company = await servise.create(db, obj_in)

    logger.debug(f"{company=}")

    return company


@router.get("/{key_id}")
async def get_key(key_id: int,
                  db: asyncpg.Pool = Depends(get_db),
                  ) -> Key:
    # user_entries = get_entries_from_collection("users")
    logger.debug("endpoint /get_key/ called")
    logger.debug(f"{db=}")
    key = await servise.get(db, key_id)

    logger.debug(f"{key=}")

    return key


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_key(key_id: int,
                     db: asyncpg.Pool = Depends(get_db),
                     ):
    logger.debug("endpoint /get_company/ called")
    company = await servise.delete_key(db, key_id)

    logger.debug(f"{company=}")
