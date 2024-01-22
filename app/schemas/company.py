from pydantic import BaseModel
from .users import User
from .address import Address


class CompanyCreate(BaseModel):
    name: str
    vat: str


class Company(CompanyCreate):
    id: int
    address: Address

    class Config():
        orm_mode = True
