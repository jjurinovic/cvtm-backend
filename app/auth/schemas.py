from pydantic import BaseModel
from typing import Optional
from ..schemas.users import UserWithCompany


class Login(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user: UserWithCompany


class TokenData(BaseModel):
    username: Optional[str] = None
