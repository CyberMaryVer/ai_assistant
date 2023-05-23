from fastapi import APIRouter

from fastapi_app.routes import api_routes, file_routes, user_routes, healthcheck, db_routes
from fastapi_app.routes.companies import path as companies

router = APIRouter()
router.include_router(api_routes.router, tags=["assistant"])
router.include_router(file_routes.router, tags=["files"], prefix="/files")
router.include_router(db_routes.router, tags=["tables"], prefix="/tables")
router.include_router(user_routes.router, tags=["users"], prefix="/users")
router.include_router(healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")

router.include_router(companies.router, tags=["companies"], prefix="/companies")