from datetime import datetime, timedelta
from enum import Enum
from typing import Union

from pydantic import BaseModel, validator

valid_values = ["general", "topic", "sources"]


class KeyBase(BaseModel):
    company_id: int
    key_type: Union[str, None] = "general"
    is_disabled: Union[bool, None] = False

    @validator('key_type')
    def key_type_valid(cls, v):
        if v not in valid_values:
            raise ValueError('Недопустимое значение')
        return v


class KeyCreate(KeyBase):
    expired_at: Union[datetime, None] = datetime.utcnow() + timedelta(days=30)


class KeyUpdate(KeyBase):
    expired_at: Union[datetime, None]


class Key(KeyBase):
    id: int
    key_id: str
    created_at: datetime
    expired_at: datetime
    usages_left: int

    class Config:
        orm_mode = True
