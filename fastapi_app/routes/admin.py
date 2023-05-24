from fastapi import APIRouter

from fastapi_app.routes.companies import path as companies
from fastapi_app.routes.keys import path as keys

router = APIRouter()

router.include_router(companies.router, tags=["companies"], prefix="/companies")
router.include_router(keys.router, tags=["api_keys"], prefix="/api_keys")
