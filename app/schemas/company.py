from pydantic import BaseModel
from .address import Address
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    vat: Optional[str] = None
    address: Address


class Company(CompanyCreate):
    id: int
    vat: Optional[str]
    address: Optional[Address] = None

    class Config():
        from_attributes = True
