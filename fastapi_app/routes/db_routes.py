from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
import asyncpg

from fastapi_app.core.db import get_db

router = APIRouter()


class Request(BaseModel):
    id: int
    timestamp: datetime
    company_id: int
    user_id: str
    chat_id: str
    raw_request: str
    filter_id: int
    timestamp_filter: datetime
    parent_response_id: int
    status: str


@router.get("/requests/", response_model=List[Request], include_in_schema=True)
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch('SELECT * FROM requests')
    return result


@router.get("/companies/", include_in_schema=True)
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch('SELECT * FROM companies')
    return result


@router.get("/keys/", include_in_schema=True)
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch('SELECT * FROM api_keys')
    return result


@router.get("/list_db_tables/", include_in_schema=True)
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")

    if not result:
        return {"message": "No tables found in the 'pgdatabase' database."}

    return {"db_tables": [record['tablename'] for record in result]}


@router.get("/show_db_tables/", include_in_schema=False)
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch("SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public'")

    if not result:
        return {"message": "No tables found in the 'pgdatabase' database."}

    return {"db_tables": result}


@router.get("/list_all_db_tables/", include_in_schema=False)
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch("SELECT * FROM pg_catalog.pg_tables")

    return result


@router.get("/check_tables/", include_in_schema=False)
async def check_tables(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        # Define the schema and table names you want to check
        schema_name = "public"
        table_names = ["users", "companies", "api_keys"]

        # Check if the tables exist in the specified schema
        exists = []
        for table_name in table_names:
            query = f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = $1 AND tablename = $2"
            result = await connection.fetchval(query, schema_name, table_name)
            exists.append(result is not None)

    if all(exists):
        return {"message": "All tables exist."}
    else:
        missing_tables = [table_name for table_name, table_exists in zip(table_names, exists) if not table_exists]
        return {"message": f"Tables not found: {', '.join(missing_tables)}"}
