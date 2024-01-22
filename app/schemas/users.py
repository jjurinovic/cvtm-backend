from pydantic import BaseModel
from typing import Optional
from .address import Address


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    company_id: Optional[int] = None
    role: int = 3
    address: Optional[Address]


class User(BaseModel):
    id: int
    name: str
    email: str
    role: int = 3
    company_id: Optional[int] = None
    address: Optional[Address]

    class Config():
        orm_mode = True
