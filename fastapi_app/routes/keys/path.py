import asyncpg
from fastapi import Depends, APIRouter, Request
from loguru import logger

from .schemas import Key, KeyCreate
from .servies import key_servise as servise

router = APIRouter()


async def get_db(request: Request) -> asyncpg.Pool:
    return request.app.state.pool


@router.get("/")
async def get_keys(db: asyncpg.Pool = Depends(get_db),
                   ) -> list[Key]:
    # user_entries = get_entries_from_collection("users")
    logger.debug("endpoint /db_users/ called")
    logger.debug(f"{db=}")
    companies = await servise.get_many(db)

    logger.debug(f"{companies=}")

    return companies


@router.post("/")
async def create_key(obj_in: KeyCreate,
                     db: asyncpg.Pool = Depends(get_db),
                     ) -> Key:
    company = await servise.create(db, obj_in)

    logger.debug(f"{company=}")

    return company
