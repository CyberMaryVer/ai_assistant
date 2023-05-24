from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from fastapi_app.routes.keys.schemas import Key


class CompanyBase(BaseModel):
    name: str
    is_disabled: bool | None = False
    email: str | None
    website: str | None
    telephone: str | None
    description: str | None


class CompanyCreate(CompanyBase):
    pass

    class Config:
        orm_mode = True


class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime
    keys: list[Key] | None

    class Config:
        orm_mode = True
