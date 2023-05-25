from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.fields import DeferredType
from typing import ForwardRef

from fastapi_app.routes.keys.schemas import Key


class UserRequestBase(BaseModel):
    raw_text: str


status_list = ["received", "filtered_rejected", "filtered_timeout", "Аccepted",
               "Response Generation Error", "Meaningless Request", "answered"]


class UserRequestCreate(UserRequestBase):
    company_id: int
    user_id: str | None
    chat_id: str | None
    status: str
    parent_id: int | None = None


class UserRequest(UserRequestCreate):
    id: int
    timestamp: datetime
    filter_id: int | None
    timestamp_filter: datetime | None
    parent_id: int | None = None

    class Config:
        orm_mode = True

UserRequestRef = ForwardRef("UserRequestPerent")
class UserRequestPerent(UserRequest):
    clarify: list[UserRequestRef]  | None = None

UserRequestPerent.update_forward_refs()