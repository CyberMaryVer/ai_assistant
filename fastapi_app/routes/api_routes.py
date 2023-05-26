import json
from typing import Any
from pydantic import BaseModel
from time import time
from fastapi import Depends, Query, APIRouter, Body, Response
from fastapi.responses import HTMLResponse

from fastapi_app.utils.logger import setup_logging
from fastapi_app.responses.api_responses import CHAT_RESPONSES, CHAT_RESPONSES_SIMPLE
from fastapi_app.chatbot.assistant import get_answer_simple
from fastapi_app.chatbot.custom_langchain import answer_with_openai
from fastapi_app.chatbot.secret import OPENAI_API_KEY  # TODO: remove this after testing

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
    api_key: str = Query(OPENAI_API_KEY, description="API key")
    topic: str = Query('business', example='tk', description="Choose topic: [business, tk, events]")
    update_sources: bool = Query(False, description="Update sources")


class DebugParams(QuestionParams):
    html: bool = Query(False, description="Generate html")
    verbose: bool = Query(False, description="Verbose")
    temperature: float = Query(0.01, description="Temperature")


def _second_chance(answer, sources, user_input, api_key):
    print("\033[095msecond chance:\033[0m", answer)
    if "нет информации" in answer.lower() or "в данном контексте" in answer.lower():
        try:
            prompt = f"Назови один-два сайта с информацией о том, "
            answer = get_answer_simple(question=user_input, prompt=prompt, api_key=api_key)
            answer = "В данной тематике нет такой информации. Могу порекомендовать поискать тут:\n" \
                     + answer["answer"]
            sources = ["https://www.google.com/",]
            return answer, sources
        except Exception as e:
            print(f"[{__name__}] Error decoding: {e}")
            return answer, sources
    else:
        return answer, sources


@router.post('/chatbot_simple/{user_id}', include_in_schema=True, responses=CHAT_RESPONSES_SIMPLE)
async def ask_chatbot(
        user_id: str,
        user_input: str = Body(..., example="How are you?", description="User text input", max_length=1500),
        question: QuestionParams = Body(...),
):
    """
    API endpoint for AI assistant (simple version)
    """
    config = {"user_id": user_id,
              "user_input": user_input,
              "topic": question.topic,
              "api_key": question.api_key,
              }
    print("user request:", config)
    result = get_answer_simple(question=user_input, api_key=question.api_key)
    try:
        pass
    except Exception as e:
        print(f"Error decoding: {e}")

    return PrettyJSONResponse(content=result)


@router.post('/chatbot_topic/{user_id}', include_in_schema=True, responses=CHAT_RESPONSES)
async def main_endpoint(
        user_id: str,
        user_input: str = Body(..., example="How are you?", description="User text input", max_length=1500),
        params: QuestionParams = Body(...),
):
    """
    API endpoint for AI assistant (advanced version)
    """

    config = {
        "user_id": user_id,
        "user_input": user_input,
        "api_key": params.api_key,
        "topic": params.topic,
        "generate_html": False,
        "verbose": False
    }
    print("user request:", config)

    start_time = time()
    answer, sources = answer_with_openai(question=user_input, api_key=params.api_key)
    answer, sources = _second_chance(answer, sources, user_input, params.api_key)
    elapsed_time = time() - start_time

    response_content = {"answer": answer, "sources": sources,
                        "user_id": user_id, "user_input": user_input,
                        "elapsed_time": elapsed_time}

    return PrettyJSONResponse(content=response_content)
