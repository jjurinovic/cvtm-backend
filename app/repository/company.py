from sqlalchemy.orm import Session
from .. import models, roles
from fastapi import HTTPException, status
from ..schemas.company import Company, CompanyCreate
from ..schemas.users import User
from .address import update_address
from datetime import datetime
from sqlalchemy import desc
from ..services import company as company_service


def create_company(req: CompanyCreate, db: Session, current_user: User) -> Company:
    address = models.Address(address1=req.address.address1, address2=req.address.address2, city=req.address.city,
                             county=req.address.county, country=req.address.country, postcode=req.address.postcode)
    db.add(address)
    db.commit()
    new_company = models.Company(name=req.name, vat=req.vat, address=address,
                                 updated_date=datetime.now(), updated_by=current_user.id)
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
    company = company_service.find_company_by_id(id, db)

    return company


def get_all_companies(db: Session):
    return db.query(models.Company).order_by(desc(models.Company.updated_date))


def update_company(req: Company, db: Session, current_user: User):
    # don't allow to return company if company not belongs to admin or user is not root
    if req.id != current_user.company_id and current_user.role != roles.Role.ROOT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden")

    # find compy by id
    company = company_service.find_company_by_id(req.id, db)

    company_data = req.model_dump(exclude_unset=True)

    if (company.address):
        company.address = update_address(company.address, req.address, db)

    company = company_service.set_updated(company, current_user)

    for key, value in company_data.items():
        setattr(company, key, value) if key != 'address' else None

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def delete_company(id: int, db: Session):
    # find compy by id
    company = company_service.find_company_by_id(id, db)

    db.delete(company)
    db.commit()
    return {"detail": "Company successfully deleted"}


def change_company_status(id: int, db: Session, current_user: User) -> Company:
    # find compy by id
    company = company_service.find_company_by_id(id, db)

    company.inactive = not company.inactive

    company = company_service.set_updated(company, current_user)

    db.add(company)
    db.commit()
    db.refresh(company)

    return company
