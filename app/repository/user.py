from sqlalchemy.orm import Session
from .. import models, hashing, roles
from fastapi import HTTPException, status
from ..schemas.users import User, UserCreate
from typing import List
from ..services.company import is_user_in_company
from ..services.user import is_email_taken, is_root, is_user, is_id_same


def create_user(req: UserCreate, db: Session, current_user: User) -> User:

    if is_email_taken(req.email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email is already taken")

    # don't allow admin to create user to another company
    if not is_user_in_company(req.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    hashed_pwd = hashing.Hash.bcrypt(req.password)
    address = models.Address(address1=req.address.address1, address2=req.address.address2, city=req.address.city,
                             county=req.address.county, country=req.address.country, postcode=req.address.postcode)
    db.add(address)
    db.commit()
    new_user = models.User(name=req.name, email=req.email,
                           password=hashed_pwd, role=req.role, company_id=req.company_id, address_id=address.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session, current_user: User) -> User:
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"User with id {id} not found")

    if is_user(current_user) and not is_id_same(id, current_user.id):
        raise not_found_exception

    user = db.query(models.User).filter(models.User.id == id).first()

    if is_root(current_user):
        return user

    if is_user_in_company(user.company_id, current_user) or not user:
        raise not_found_exception

    return user


def get_all_users(company_id: int, db: Session, current_user) -> List[User]:
    # don't allow admin to create user to another company
    if not is_user_in_company(company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    return db.query(models.User).filter(models.User.company_id == company_id)


def create_root(req: UserCreate, db: Session) -> User:
    hashed_pwd = hashing.Hash.bcrypt(req.password)
    new_user = models.User(name=req.name, email=req.email,
                           password=hashed_pwd, role=roles.Role.ROOT.value, company_id=None)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
