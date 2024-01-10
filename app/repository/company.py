from sqlalchemy.orm import Session
from .. import models, schemas, roles
from fastapi import HTTPException, status


def create_company(req: schemas.Company, db: Session):
    new_company = models.Company(name=req.name, vat=req.vat)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(id: int, db: Session, current_user: schemas.User):
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
    return db.query(models.Company).all()
