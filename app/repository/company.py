from sqlalchemy.orm import Session
from .. import models, roles
from fastapi import HTTPException, status
from ..schemas.company import Company, CompanyCreate
from ..schemas.users import User
from .address import update_address


def create_company(req: CompanyCreate, db: Session) -> Company:
    address = models.Address(address1=req.address.address1, address2=req.address.address2, city=req.address.city,
                             county=req.address.county, country=req.address.country, postcode=req.address.postcode)
    db.add(address)
    db.commit()
    new_company = models.Company(name=req.name, vat=req.vat, address=address)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(id: int, db: Session, current_user: User):
    # don't allow to return company if company not belongs to admin or user is not root
    if id != current_user.company_id and current_user.role != roles.Role.ROOT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden")

    # find compy by id
    company = db.query(models.Company).filter(models.Company.id == id).first()

    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company with id {id} not found")

    return company


def get_all_companies(db: Session):
    return db.query(models.Company)


def update_company(req: Company, db: Session, current_user: User):
    # don't allow to return company if company not belongs to admin or user is not root
    if req.id != current_user.company_id and current_user.role != roles.Role.ROOT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden")

    # find compy by id
    company = db.query(models.Company).filter(
        models.Company.id == req.id).one_or_none()

    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company with id {id} not found")

    company_data = req.model_dump(exclude_unset=True)

    if (company.address):
        company.address = update_address(company.address, req.address, db)

    for key, value in company_data.items():
        setattr(company, key, value) if key != 'address' else None

    db.add(company)
    db.commit()
    db.refresh(company)
    return company
