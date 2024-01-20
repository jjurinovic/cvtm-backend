from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    company_id: Optional[int] = None
    role: int = 3


class User(BaseModel):
    id: int
    name: str
    email: str
    role: int = 3
    company_id: Optional[int] = None

    class Config():
        orm_mode = True
