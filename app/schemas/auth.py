from pydantic import BaseModel
from typing import Optional
from ..schemas.users import User


class Login(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user: User


class TokenData(BaseModel):
    username: Optional[str] = None
