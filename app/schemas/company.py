from pydantic import BaseModel
from .address import Address
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    vat: Optional[str] = None
    address: Address


class Company(CompanyCreate):
    id: int
    vat: Optional[str]
    address: Optional[Address] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    inactive: bool = False
    updated_by: Optional[int] = None

    class Config():
        from_attributes = True
