from fastapi import APIRouter

from fastapi_app.routes import api_routes, healthcheck

router = APIRouter()
router.include_router(api_routes.router, tags=["assistant"])
router.include_router(healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")

