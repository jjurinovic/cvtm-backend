from pydantic import BaseModel
from .address import Address
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    vat: str
    address: Address


class Company(CompanyCreate):
    id: int
    address: Optional[Address] = None

    class Config():
        from_attributes = True
