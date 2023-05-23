from fastapi import APIRouter

from fastapi_app.routes.companies import path as companies

router = APIRouter()

router.include_router(companies.router, tags=["companies"], prefix="/companies")