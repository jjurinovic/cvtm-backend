from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import Address
from .. import models
from .exceptions import AddressNotFound


class AddressRepository:
    db: Session

    def __init__(
        self,
        db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    def create(self, address: Address):
        new_address = models.Address(
            address1=address.address1,
            address2=address.address2,
            city=address.city,
            county=address.county,
            country=address.country,
            postcode=address.postcode
        )

        self.db.add(new_address)
        self.db.commit()
        self.db.refresh(new_address)
        return new_address

    def update(self, req: Address):
        address = self.db.query(models.Address).filter(
            models.Address.id == req.id).first()

        if not address:
            raise AddressNotFound()

        address_data = req.model_dump(exclude_unset=True)

        for key, value in address_data.items():
            setattr(address, key, value)

        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address
