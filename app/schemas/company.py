from pydantic import BaseModel
from .address import AddressSchema
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    vat: str


class Company(CompanyCreate):
    id: int
    address: Optional[AddressSchema] = None

    class Config():
        from_attributes = True
