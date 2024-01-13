from pydantic import BaseModel
from typing import List
from .users import User


class CompanyCreate(BaseModel):
    name: str
    vat: str


class Company(CompanyCreate):
    id: int
    employees: List[User]

    class Config():
        orm_mode = True
