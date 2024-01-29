from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    address1: str
    address2: Optional[str] = None
    city: str
    county: Optional[str] = None
    country: str
    postcode: str

    class Config():
        from_attributes = True
