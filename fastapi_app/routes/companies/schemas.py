from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from fastapi_app.routes.keys.schemas import Key


class CompanyBase(BaseModel):
    name: str
    is_disabled: bool = False
    email: Union[str, None]
    website: Union[str, None]
    telephone: Union[str, None]
    description: Union[str, None]


class CompanyCreate(CompanyBase):
    pass

    class Config:
        orm_mode = True


class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime
    # keys: Union[list[Key], None]

    class Config:
        orm_mode = True
