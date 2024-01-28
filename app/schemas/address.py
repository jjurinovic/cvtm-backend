from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    postcode: Optional[str] = None

    class Config():
        from_attributes = True
