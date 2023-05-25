from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from fastapi_app.routes.keys.schemas import Key


class FilterBase(BaseModel):
    description: str | None


class FilterCreate(FilterBase):
    word: str
    company_id: int
    created_user_id: str | None
    is_archive: bool = False


class FilterInCreate(FilterBase):
    word: str


class FilterUpdate(FilterBase):
    pass


class FilterArchive(FilterBase):
    is_archive: bool = True
    archive_at: datetime | None
    archive_user_id: str | None


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
    description: str | None
    is_archive: bool

    class Config:
        orm_mode = True
