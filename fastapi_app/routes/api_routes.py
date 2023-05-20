import json
from typing import Any
from pydantic import BaseModel
from fastapi import Depends, Query, APIRouter, Body, Response
from fastapi.responses import HTMLResponse

from fastapi_app.utils.logger import setup_logging
from fastapi_app.responses.api_responses import CHAT_RESPONSES

router = APIRouter()
logger = setup_logging()


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


class QuestionParams(BaseModel):
    topic: bool = Query(False, description="Enable topic")
    api_key: str = Query(..., description="API key", max_length=100)


@router.post('/chatbot/{user_id}', include_in_schema=True, responses=CHAT_RESPONSES)
async def ask_chatbot(
        user_id: str,
        user_input: str = Body(..., example="How are you?", description="User text input", max_length=1500),
        question: QuestionParams = Body(...),
):
    """
    AI assistant API endpoint

    For more details, check out the [API documentation](https://api.aiengineers.com/redoc#tag/chat/operation/chatbot)

    """

    config = {"user_id": user_id,
              "user_input": user_input,
              "topic": question.topic,
              "api_key": question.api_key,
              }
    print("user request:", config)
    # result = get_result(config)
    result = config
    try:
        pass
    except Exception as e:
        print(f"Error decoding: {e}")

    return PrettyJSONResponse(content=result)


@router.get("/", include_in_schema=False)
async def root():
    body = """<html>
           <body style='padding: 10px;'>
           <h1>FastAPI pipeline</h1>
           <div>
           </div>
           </body>
           </html>"""

    return HTMLResponse(content=body)
