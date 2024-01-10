from pydantic import BaseModel
from typing import List
from typing import Optional
from .roles.roles import Role


class Company(BaseModel):
    name: str
    vat: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    company: List[Company]

    class Config():
        orm_mode = True


class ShowCompany(Company):
    id: int
    creator: ShowUser

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
    role: str = Role.USER