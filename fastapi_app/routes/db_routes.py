from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List
import asyncpg

router = APIRouter()


class User(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    telephone: str
    company_id: int
    created_at: str


# Depend on the Request to access app state
async def get_db(request: Request) -> asyncpg.Pool:
    return request.app.state.pool


@router.get("/users/", response_model=List[User])
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch('SELECT * FROM users')
    return result


@router.get("/companies/")
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch('SELECT * FROM companies')
    return result


@router.get("/keys/")
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch('SELECT * FROM api_keys')
    return result


@router.get("/list_db_tables/")
async def read_items(db: asyncpg.Pool = Depends(get_db)):
    async with db.acquire() as connection:
        result = await connection.fetch("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")

    if not result:
        return {"message": "No tables found in the 'pgdatabase' database."}

    return {"db_tables": [record['tablename'] for record in result]}


@router.get("/show_db_tables/")
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
