import datetime

import asyncpg
from fastapi import Depends, APIRouter, Header
from loguru import logger
from starlette import status
from starlette.background import BackgroundTasks

from ..user_requests.schemas import UserRequestBase, UserRequestCreate, UserRequestOut
from ..user_requests.servies import generate_clarify_response, user_requests_servise
from ...core.db import get_db
from .schemas import UserResponse, Feedback, FeedbackCreate, FeedbackIn
from .servies import user_response_servise as servise
from .servies_feedback import feedback_servise
from ..companies.schemas import Company
from ...utils.auth import get_current_active_company

router = APIRouter()


@router.get("/{respons_id}")
async def get_request(respons_id: int,
                      company: Company = Depends(get_current_active_company),
                      user_id: str = Header(None),
                      db: asyncpg.Pool = Depends(get_db),
                      ) -> UserResponse:
    """Получить ответ"""
    logger.info(f"[Response] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj = await servise.get_by_company(db, respons_id, company.id)
    logger.debug(f"{obj=}")

    return obj


@router.post("/{respons_id}/clarify")
async def clarify_response(background_tasks: BackgroundTasks,
                           respons_id: int,
                           obj_in: UserRequestBase,
                           user_id: str = Header(None),
                           chat_id: str = Header(None),
                           company: Company = Depends(get_current_active_company),
                           db: asyncpg.Pool = Depends(get_db),
                           ) -> UserRequestOut:
    """Задать уточненяющий вопрос"""
    logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj_save = UserRequestCreate(**obj_in.dict(),
                                 parent_resp_id=respons_id,
                                 company_id=company.id,
                                 user_id=user_id,
                                 chat_id=chat_id,
                                 status="received")

    obj = await user_requests_servise.save(db, obj_save)
    obj = await user_requests_servise.request_processing(db, obj)

    background_tasks.add_task(generate_clarify_response, db, obj)

    return obj


@router.get("/{respons_id}/feedback")
async def get_feedback(respons_id: int,
                       user_id: str = Header(None),
                       company: Company = Depends(get_current_active_company),
                       db: asyncpg.Pool = Depends(get_db),
                       ) -> list[Feedback]:
    """Получить оценки на ответ"""
    logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")

    feedbacks = await feedback_servise.get_by_company(db, respons_id, company.id)

    return feedbacks


@router.post("/{respons_id}/feedback")
async def feedback_response(respons_id: int,
                            obj_in: FeedbackIn,
                            user_id: str = Header(None),
                            company: Company = Depends(get_current_active_company),
                            db: asyncpg.Pool = Depends(get_db),
                            ) -> Feedback:
    """оценить ответ"""
    logger.info(f"[Request] {user_id=} сделал запрос от Компании: '{company.name}'")

    obj_save = FeedbackCreate(**obj_in.dict(),
                              respons_id=respons_id,
                              user_id=user_id
                              )

    feedback = await feedback_servise.save(db, obj_save, company.id)

    return feedback
