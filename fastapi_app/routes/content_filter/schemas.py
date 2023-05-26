from datetime import datetime
from typing import Union

from pydantic import BaseModel, validator

from fastapi_app.routes.keys.schemas import Key


class FilterBase(BaseModel):
    description: Union[str, None]


class FilterCreate(FilterBase):
    word: str
    company_id: int
    created_user_id: Union[str, None]
    is_archive: bool = False


class FilterInCreate(FilterBase):
    word: str

    @validator('word')
    def key_type_valid(cls, v):
        if len(v.strip().split()) != 1 :
            raise ValueError('Передайте только 1 слово.')
        return v.strip()


class FilterUpdate(FilterBase):
    pass


class FilterArchive(FilterBase):
    is_archive: bool = True
    archive_at: Union[datetime, None] = datetime.utcnow()
    archive_user_id: Union[str, None]


class Filter(FilterBase):
    id: int
    word: str
    created_at: datetime
    company_id: int
    is_archive: bool
    class Config:
        orm_mode = True


class FilterOut(BaseModel):
    id: int
    word: str
    created_at: datetime
    description: Union[str, None]
    is_archive: bool

    class Config:
        orm_mode = True
