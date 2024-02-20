from pydantic import BaseModel
from typing import Optional
from ..users.schemas import UserWithCompany


class Login(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user: UserWithCompany


class TokenData(BaseModel):
    username: Optional[str] = None
