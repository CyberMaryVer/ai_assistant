from fastapi import Depends, APIRouter, Query
from starlette.responses import FileResponse

router = APIRouter()


@router.get("/", include_in_schema=True)
async def root():
    # return {"message": "Hello World"}
    return FileResponse("./fastapi_app/static/index.html")