import json
import os
from fastapi import HTTPException
from typing import Any
from pydantic import BaseModel
from time import time
from fastapi import Query, APIRouter, Body, Response
from starlette import status

from fastapi_app.utils.logger import setup_logging
from fastapi_app.responses.api_responses import CHAT_RESPONSES, CHAT_RESPONSES_SIMPLE
from fastapi_app.chatbot.assistant import get_answer_simple
from fastapi_app.chatbot.custom_langchain import answer_with_openai
from fastapi_app.chatbot.update_sources import add_tk_sources
from fastapi_app.chatbot.fake_keys.validate_key import use_key

# from fastapi_app.chatbot.secret import OPENAI_API_KEY  # TODO: remove this after testing


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "OPENAI_API_KEY")
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
    tada_key: str = Query(..., description="Tada key")
    topic: str = Query('business', example='tk', description="Choose topic: [business, tk, events]")
    enrich_sources: bool = Query(False, description="Add links to sources (tk only)")


class QuestionParamsSimple(BaseModel):
    tada_key: str = Query(..., description="API key")


class DebugParams(QuestionParams):
    api_key: str = Query(OPENAI_API_KEY, description="API key")
    html: bool = Query(False, description="Generate html")
    verbose: bool = Query(False, description="Verbose")
    temperature: float = Query(0.01, description="Temperature")
    return_context: bool = Query(False, description="Return context")


def _get_valid_key(key):
    key_status = use_key(key)
    if 'success' in key_status:
        return OPENAI_API_KEY, key_status['uses_left']
    else:
        return None, key_status['error']


def _second_chance(answer, sources, user_input, api_key):
    print("\033[095msecond chance:\033[0m", answer)

    is_answer_ok = ["нет информации" in answer.lower(),
                    "в данном контексте" in answer.lower(),
                    "данной информации в контексте не приведено" in answer.lower(),
                    "невозможно дать точный ответ" in answer.lower(),
                    "невозможно дать ответ" in answer.lower(),
                    "контекст не содержит информации" in answer.lower()]

    if any(is_answer_ok):
        try:
            prompt = f"Назови пару источников, где можно найти информацию о том, "
            second_answer = get_answer_simple(question=user_input, prompt=prompt, api_key=api_key)
            second_answer = answer + " Могу порекомендовать поискать тут:\n" + second_answer["answer"]
            sources = sources + ["https://www.google.com/", ]
            return second_answer, sources

        except Exception as e:
            print(f"[{__name__}] Error decoding: {e}")
            return answer, sources

    else:
        return answer, sources


@router.post('/chatbot_simple/{user_id}', include_in_schema=True, responses=CHAT_RESPONSES_SIMPLE)
async def ask_chatbot(
        user_id: str,
        user_input: str = Body('как начисляется ндфл сотруднику работающему из другой страны',
                               example="How are you?",
                               description="User text input",
                               max_length=500),
        params: QuestionParamsSimple = Body(...),
):
    """
    API endpoint for AI assistant (simple version)
    """
    api_key, uses_left = _get_valid_key(params.tada_key)
    if api_key is None:
        return PrettyJSONResponse(content={"error": "Your key is invalid or expired",
                                           "key_status": uses_left})

    config = {"user_id": user_id,
              "user_input": user_input,
              "user_key": params.tada_key,
              }
    print("user request:", config)

    start_time = time()
    result = get_answer_simple(question=user_input, api_key=api_key)
    elapsed_time = time() - start_time

    try:
        result.update({"user_request": config, "key_status": uses_left, "elapsed_time": elapsed_time})
    except Exception as e:
        print(f"Error decoding: {e}")

    logger.info(f"response: {result}")
    return PrettyJSONResponse(content=result)


@router.post('/chatbot_topic/{user_id}', include_in_schema=True, responses=CHAT_RESPONSES)
async def ask_assistant(
        user_id: str,
        user_input: str = Body('как начисляется ндфл сотруднику работающему из другой страны',
                               example="How are you?",
                               description="User text input",
                               max_length=1500),
        params: QuestionParams = Body(...),
):
    """
    API endpoint for AI assistant (advanced version)
    """
    api_key, uses_left = _get_valid_key(params.tada_key)
    if api_key is None:
        return PrettyJSONResponse(content={"error": "Your key is invalid or expired",
                                           "key_status": uses_left})
    config = {
        "user_input": user_input,
        "topic": params.topic,
        "user_id": user_id,
        "user_key": params.tada_key,
        # "generate_html": False,
        # "verbose": False
    }
    print("user request:", config)

    start_time = time()
    answer, sources = answer_with_openai(question=user_input, api_key=api_key, faiss_index=params.topic)
    answer, sources = _second_chance(answer, sources, user_input, api_key)
    elapsed_time = time() - start_time

    if params.enrich_sources and params.topic == 'tk':
        sources = add_tk_sources(sources)

    response_content = {"answer": answer, "sources": sources, "user_request": config, "uses_left": uses_left,
                        "elapsed_time": elapsed_time}

    logger.info(f"response: {response_content}")
    return PrettyJSONResponse(content=response_content)


async def calling_assistant(user_input: str, topic: str = "default", enrich_sources: bool = True,
                            tada_key: str = "ratelimit"):
    api_key, uses_left = _get_valid_key(tada_key)
    if api_key is None:
        logger.warning("Превышено лимит запросов, попробуйте позже")
        raise PermissionError("Превышено лимит запросов, попробуйте позже")

    answer, sources = answer_with_openai(question=user_input, api_key=api_key, faiss_index=topic)
    answer, sources = _second_chance(answer, sources, user_input, api_key)

    if enrich_sources and topic == 'tk':
        sources = add_tk_sources(sources)

    response_content = {"answer": answer, "sources": sources}
    logger.info(f"response: {response_content}, {uses_left=}")

    return response_content
