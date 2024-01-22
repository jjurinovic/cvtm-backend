from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    address1: Optional[str]
    address2: Optional[str]
    city: Optional[str]
    county: Optional[str]
    country: Optional[str]
    postcode: Optional[str]
