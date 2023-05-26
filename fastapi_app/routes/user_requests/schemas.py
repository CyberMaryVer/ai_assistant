from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel
from pydantic.fields import DeferredType
from typing import ForwardRef

from fastapi_app.routes.keys.schemas import Key

example = "Я вижу большую кошку на дереве."

status_list = {"received": "Вопрос получен",
               "filtered_rejected": "Вопрос не прошол фильтры",
               "filtered_timeout": "превышено время проверки фильтрами",
               "accepted": "Вопрос принят",
               "response_generation_error": "Произошла ошибка при генераци ответа",
               "meaningless_request": "Вопрос не имеет смысла",
               "answered": "Ответ предоставлен"}


class UserRequestBase(BaseModel):
    raw_text: str = Query(example, description="Вопрос пользователя")


class UserRequestCreate(UserRequestBase):
    company_id: int
    user_id: str | None
    chat_id: str | None
    status: str
    response_id: int | None = None

class UserRequestUpdate(BaseModel):
    status: str
    filter_id: int | None = None
    timestamp_filter: datetime | None = None


class UserRequest(UserRequestCreate):
    id: int
    timestamp: datetime
    filter_id: int | None
    timestamp_filter: datetime | None

    class Config:
        orm_mode = True
        exclude = {'id'}


class UserRequestOut(BaseModel):
    raw_text: str
    id: int
    user_id: str
    status: str
    timestamp: datetime
    filter_id: int | None
    timestamp_filter: datetime | None

    class Config:
        orm_mode = True
        exclude = {'id'}


class UserRequestDialog(UserRequest):
    response: list[dict] | None

# UserRequestRef = ForwardRef("UserRequestPerent")
# class UserRequestPerent(UserRequest):
#     clarify: list[UserRequestRef]  | None = None
#
# UserRequestPerent.update_forward_refs()
