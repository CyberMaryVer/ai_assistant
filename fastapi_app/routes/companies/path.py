import asyncpg
from fastapi import Depends, APIRouter, Request
from loguru import logger
from starlette import status

from ...core.db import get_db
from .schemas import Company, CompanyCreate
from .servies import company_servise
from ..keys.schemas import Key


router = APIRouter()




@router.get("")
async def get_companies(db: asyncpg.Pool = Depends(get_db),
                        ) -> list[Company]:
    # user_entries = get_entries_from_collection("users")
    logger.debug("endpoint /db_users/ called")
    logger.debug(f"{db=}")
    companies = await company_servise.get_many(db)

    logger.debug(f"{companies=}")

    # return {"rwer": "wer"}
    return companies


@router.post("")
async def create_company(obj_in: CompanyCreate,
                         db: asyncpg.Pool = Depends(get_db),
                         ) -> Company:
    company = await company_servise.create(db, obj_in)

    logger.debug(f"{company=}")

    return company


@router.get("/{company_id}/api_keys")
async def get_company_keys(company_id: int,
                           db: asyncpg.Pool = Depends(get_db),
                           ) -> list[Key]:
    logger.debug("endpoint /get_company/ called")
    kyes = await company_servise.get_kyes(db, company_id)

    logger.debug(f"{kyes=}")

    return kyes


@router.get("/{company_id}")
async def get_company(company_id: int,
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> Company:
    logger.debug("endpoint /get_company/ called")
    company = await company_servise.get(db, company_id)

    logger.debug(f"{company=}")

    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int,
                      db: asyncpg.Pool = Depends(get_db),
                      ):
    logger.debug("endpoint /get_company/ called")
    company = await company_servise.delete_company(db, company_id)

    logger.debug(f"{company=}")
