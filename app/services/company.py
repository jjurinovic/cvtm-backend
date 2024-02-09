from ..schemas.users import User
from ..roles import Role
from datetime import datetime
from ..schemas.company import Company
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Company as CompanyModel


def is_user_in_company(company_id: int, current_user: User) -> bool:
    return company_id == current_user.company_id or current_user.role == Role.ROOT


def set_updated(company: Company, current_user: User):
    company.updated_date = datetime.now()
    company.updated_by = current_user.id
    return company


def find_company_by_id(id: int, db: Session) -> Company:
    company = db.query(CompanyModel).filter(CompanyModel.id == id).first()

    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Company with id {id} not found")

    return company
