from fastapi import APIRouter

from fastapi_app.routes import api_routes, file_routes, db_routes, healthcheck

router = APIRouter()
router.include_router(api_routes.router, tags=["assistant"])
router.include_router(file_routes.router, tags=["files"], prefix="/files")
router.include_router(db_routes.router, tags=["users"], prefix="/users")
router.include_router(healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")