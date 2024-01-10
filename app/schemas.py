from pydantic import BaseModel
from typing import List
from typing import Optional


class Company(BaseModel):
    name: str
    vat: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    company_id: int

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
    role: str = "USER"
    company_id: int


class ShowCompany(Company):
    id: int
    employees: List[ShowUser]

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
