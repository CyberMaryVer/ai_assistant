from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    is_disabled: Optional[bool] = None


class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True
