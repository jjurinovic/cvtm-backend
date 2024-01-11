from sqlalchemy.orm import Session
from .. import models, schemas, roles
from fastapi import HTTPException, status


def create_day(req: schemas.Day, db: Session):
    new_day = models.Day(
        date=req.date, company_id=req.company_id, user_id=req.user_id)
    db.add(new_day)
    db.commit()
    db.refresh(new_day)
    return new_day


def get_day(id: int, db: Session, current_user: schemas.User):
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
