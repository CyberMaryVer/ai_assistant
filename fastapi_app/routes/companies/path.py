import asyncpg
from fastapi import Depends, APIRouter, Request
from loguru import logger

from .schemas import Company
from .servies import company_servise

router = APIRouter()


async def get_db(request: Request) -> asyncpg.Pool:
    return request.app.state.pool


@router.get("/")
async def get_companies(db: asyncpg.Pool = Depends(get_db),
                        ) -> list[Company]:
    # user_entries = get_entries_from_collection("users")
    logger.debug("endpoint /db_users/ called")
    logger.debug(f"{db=}")
    companies = await company_servise.get_many(db)

    logger.debug(f"{companies=}")

    # return {"rwer": "wer"}
    return companies
