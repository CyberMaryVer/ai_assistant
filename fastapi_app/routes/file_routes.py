from fastapi import File, UploadFile, APIRouter, Query
from fastapi.responses import HTMLResponse, FileResponse, Response
import os

from fastapi_app.utils.logger import logger


router = APIRouter()


@router.get("/file_download_json")
async def download_file_locally(file_path: str = Query(..., description="Path to the file to download")):
    logger.debug(f"Sending file {file_path} to client | endpoint: /file_download")
    return FileResponse(path=file_path, filename=file_path, media_type='json/application')


@router.post("/file_upload")
async def upload_file_locally(file: UploadFile = File(..., description="A file to read")):
    try:
        try:
            contents = file.file.read()
        except Exception as e:
            return {"error": f"[{type(e)}] {e}"}
        finally:
            file.file.close()

        file_path = f"./temp_data/{file.filename}"
        if os.path.exists(file_path):
            with open(file_path, "wb") as writer:
                writer.write(contents)
        else:
            return {"error": f"[PathError] Path doesn't exist"}

    except Exception as e:
        return {"error": f"[{type(e)}] {e}"}

    logger.debug(f"Uploaded file {file.filename} to {file_path} | endpoint: /file_upload")
    return {"filename": file.filename}