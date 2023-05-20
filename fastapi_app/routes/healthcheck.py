from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/healthcheck', status_code=200)
async def healthcheck():
    return HTMLResponse(content='The app is running and healthy')


# @router.get('/metrics', status_code=200)
# async def metrics():
#     return HTMLResponse(content='The app is running and healthy')
