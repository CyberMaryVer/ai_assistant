from datetime import datetime
from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel, conint

status_list = {"successful": "Ответ подготовлен",
               "generate_error": "Ответ не удалось сформировать",
               "timeout": "Ответ не удалось подготовить в срок",
               "requires_investigation": "Вопрос требует уточнений",
               }


class UserResponseBase(BaseModel):
    raw_text: Union[str, None]
    sources: Union[list[str], None]


class UserResponseCreate(UserResponseBase):
    request_id: int
    status: str


class UserResponse(UserResponseCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class FeedbackBase(BaseModel):
    respons_id: int
    user_id: Union[str, None] = None
    estimation: conint(ge=1, le=5)
    note: Union[str, None] = None


class FeedbackIn(BaseModel):
    estimation: conint(ge=1, le=5)
    note: Union[str, None] = Query("Ответ был очень полезен", description="Вопрос пользователя")


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# class UserRequestDialog(UserRequest):
#     response: list[dict] | None

# UserRequestRef = ForwardRef("UserRequestPerent")
# class UserRequestPerent(UserRequest):
#     clarify: list[UserRequestRef]  | None = None
#
# UserRequestPerent.update_forward_refs()
