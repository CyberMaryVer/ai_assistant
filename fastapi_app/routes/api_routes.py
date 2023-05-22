import json
from typing import Any
from pydantic import BaseModel
from fastapi import Depends, Query, APIRouter, Body, Response
from fastapi.responses import HTMLResponse

from fastapi_app.utils.logger import setup_logging
from fastapi_app.responses.api_responses import CHAT_RESPONSES
from fastapi_app.chatbot.assistant import get_answer_simple
from fastapi_app.chatbot.secret import OPEN_API_KEY  # TODO: remove this after testing

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
    sources: bool = Query(False, description="Enable sources")


@router.post('/chatbot/{user_id}{api_key}', include_in_schema=True, responses=CHAT_RESPONSES)
async def ask_chatbot(
        user_id: str,
        api_key: str,
        user_input: str = Body(..., example="How are you?", description="User text input", max_length=1500),
        question: QuestionParams = Body(...),
):
    """
    AI assistant API endpoint

    For more details, check out the [API documentation](https://api.aiengineers.com/redoc#tag/chat/operation/chatbot)

    """
    api_key = OPEN_API_KEY # TODO: remove this after testing
    config = {"user_id": user_id,
              "user_input": user_input,
              "topic": question.topic,
              "sources": question.sources,
              "api_key": api_key,
              }
    print("user request:", config)
    result = get_answer_simple(question=user_input, api_key=api_key)
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
