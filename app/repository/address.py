from ..models import Address
from ..schemas.address import Address as AddressSchema
from sqlalchemy.orm import Session


def create_address(req: AddressSchema, db: Session):
    address = Address(address1=req.address.address1, address2=req.address.address2, city=req.address.city,
                      county=req.address.county, country=req.address.country, postcode=req.address.postcode)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(address: AddressSchema, req: AddressSchema, db: Session):
    address_data = req.model_dump(exclude_unset=True)

    for key, value in address_data.items():
        setattr(address, key, value)

    db.add(address)
    db.commit()
    db.refresh(address)
    return address
