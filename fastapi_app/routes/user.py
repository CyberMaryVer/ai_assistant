from fastapi import APIRouter

from fastapi_app.routes.content_filter import path as content_filter

router = APIRouter()

router.include_router(content_filter.router, tags=["content_filter"], prefix="/content_filter")

