from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime
from sqlalchemy import desc
from typing import List

from ..database import get_db
from ..address.repository import AddressRepository
from .schemas import Company, CompanyCreate
from .. import models
from .utils import set_updated
from ..users.schemas import User
from ..auth.dependecies import get_current_user


class CompanyRepository:
    db: Session
    addressRepository: AddressRepository
    current_user: User

    def __init__(
        self,
        db: Session = Depends(get_db),
        addressRepository: AddressRepository = Depends(),
        user: User = Depends(get_current_user)
    ) -> None:
        self.db = db
        self.addressRepository = addressRepository
        self.current_user = user

    # Create Company
    def create(self, req: CompanyCreate) -> Company:
        address = self.addressRepository.create(req.address)

        new_company = models.Company(
            name=req.name,
            vat=req.vat,
            address=address,
            updated_date=datetime.now(),
            updated_by=self.current_user.id
        )

        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company

    # Get company by id
    def get(self, id: int) -> Company:
        company = self.db.query(models.Company).filter(
            models.Company.id == id).first()
        return company

    # Get all companies
    def get_all(self) -> List[Company]:
        return self.db.query(models.Company)

    # Update company
    def update(self, req: Company, company: Company) -> Company:
        company_data = req.model_dump(exclude_unset=True)

        if (company.address):
            company.address = self.addressRepository.update(req.address)
        else:
            company.address = self.addressRepository.create(req.address)

        company = set_updated(company, self.current_user)

        for key, value in company_data.items():
            setattr(company, key, value) if key != 'address' else None

        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    # Delete company
    def delete(self, company: Company):
        self.db.delete(company)
        self.db.commit()

        return {"detail": "Company successfully deleted"}

    # Change status
    def change_status(self, company: Company) -> Company:
        company.inactive = not company.inactive

        company = set_updated(company, self.current_user)

        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)

        return company
