from sqlalchemy.orm import Session
from .. import models, schemas, hashing, roles
from fastapi import HTTPException, status


def same_company_id_and_no_root(company_id, user_company_id, role) -> bool:
    if role != roles.Role.ROOT and user_company_id != company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")


def create_user(req: schemas.ShowUser, db: Session, current_user: schemas.User):

    # don't allow admin to create user to another company
    same_company_id_and_no_root(
        req.company_id, current_user.company_id, current_user.role)

    hashed_pwd = hashing.Hash.bcrypt(req.password)
    new_user = models.User(name=req.name, email=req.email,
                           password=hashed_pwd, role=req.role, company_id=req.company_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id).first()

    if current_user.role == roles.Role.ROOT:
        return user

    if user.company_id != current_user.company_id or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user


def get_all_users(company_id: int, db: Session, current_user):
    # don't allow admin to create user to another company
    same_company_id_and_no_root(
        company_id, current_user.company_id, current_user.role)

    return db.query(models.User).filter(models.User.company_id == company_id)
