from pydantic import BaseModel, EmailStr
from typing import Optional
from .address import Address


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    company_id: Optional[int] = None
    role: int = 3
    address: Optional[Address]


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: int = 3
    company_id: Optional[int] = None
    address: Optional[Address]

    class Config():
        from_attributes = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
