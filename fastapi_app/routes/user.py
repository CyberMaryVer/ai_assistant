from fastapi import APIRouter

from fastapi_app.routes.content_filter import path as content_filter
from fastapi_app.routes.user_requests import path as user_requests
from fastapi_app.routes.user_response import path as user_response

router = APIRouter()

router.include_router(content_filter.router, tags=["content_filter"], prefix="/content_filter")
router.include_router(user_requests.router, tags=["requests"], prefix="/requests")
router.include_router(user_response.router, tags=["response"], prefix="/response")
