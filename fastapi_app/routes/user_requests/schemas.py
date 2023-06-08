from datetime import datetime
from typing import Union

from fastapi import Query
from pydantic import BaseModel
from pydantic.fields import DeferredType
from typing import ForwardRef

from fastapi_app.routes.keys.schemas import Key
from fastapi_app.routes.user_response.schemas import UserResponse

example = "как начисляется ндфл сотруднику работающему из другой страны?"

status_list = {"received": "Вопрос получен",
               "filtered_rejected": "Вопрос не прошел фильтры",
               "filtered_timeout": "превышено время проверки фильтрами",
               "accepted": "Вопрос принят",
               "rate_limit": "Превышен rate_limit запросов",
               "response_generation_error": "Произошла ошибка при генерации ответа",
               "meaningless_request": "Вопрос не имеет смысла",
               "answered": "Ответ предоставлен"}


class UserRequestBase(BaseModel):
    raw_text: str = Query(example, description="Вопрос пользователя")
    topic: Union[str, None] = Query('business', example='tk', description="Choose topic: [business, tk]")


class UserRequestCreate(UserRequestBase):
    company_id: int
    user_id: Union[str, None]
    chat_id: Union[str, None]
    status: str
    parent_resp_id: Union[int, None] = None


class UserRequestUpdate(BaseModel):
    status: str
    filter_id: Union[int, None] = None
    timestamp_filter: Union[datetime, None] = None


class UserRequest(UserRequestCreate):
    id: int
    timestamp: datetime
    filter_id: Union[int, None]
    timestamp_filter: Union[datetime, None]

    class Config:
        orm_mode = True


class UserRequestOut(BaseModel):
    raw_text: str
    id: int
    user_id: Union[str, None]
    status: str
    timestamp: datetime
    filter_id: Union[int, None]
    timestamp_filter: Union[datetime, None]

    class Config:
        orm_mode = True




UserRequestRef = ForwardRef("UserResponseDialog")
class UserRequestDialog(UserRequest):
    response: Union[UserRequestRef, None] = None

class UserResponseDialog(UserResponse):
    clarify: Union[UserRequestDialog, None] = None


UserRequestDialog.update_forward_refs()





# UserRequestRef = ForwardRef("UserRequestPerent")
# class UserRequestPerent(UserRequest):
#     clarify: list[UserRequestRef]  | None = None
#
# UserRequestPerent.update_forward_refs()
