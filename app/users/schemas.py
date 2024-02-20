from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from ..address.schemas import Address
from ..company.schemas import Company


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    company_id: Optional[int] = None
    role: int = 3
    address: Optional[Address]


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password_changed: Optional[bool] = False
    role: int = 3
    company_id: Optional[int] = None
    address: Optional[Address]
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    inactive: bool = False
    updated_by: Optional[int] = None

    class Config():
        from_attributes = True


class UserWithCompany(User):
    company: Optional[Company] = None

    class Config():
        from_attributes = True


class UserWithDeleted(UserWithCompany):
    deleted: bool

    class Config():
        from_attributes = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
