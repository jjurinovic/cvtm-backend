from sqlalchemy.orm import Session
from .. import models, hashing, roles
from fastapi import HTTPException, status
from ..schemas.users import User, UserCreate, PasswordChange, UserWithDeleted
from typing import List
from ..services.company import is_user_in_company
from ..services import user as user_service
from .address import create_address, update_address
from ..hashing import Hash
from ..email.send_email import send_registration_email
import secrets
import string
from ..roles import Role
from datetime import datetime
from sqlalchemy import desc, asc


async def create_user(req: UserCreate, db: Session, current_user: User) -> User:
    # Root can only create another root
    if not user_service.is_root(current_user) and req.role == Role.ROOT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only ROOT user can create another root user")

    # check if email is already taken
    if user_service.is_email_taken(req.email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email is already taken")

    # don't allow admin to create user to another company
    if not is_user_in_company(req.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    address = None
    if (req.address):
        address = create_address(req, db)

    # create random password
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    hashed_pwd = hashing.Hash.bcrypt(password)

    new_user = models.User(first_name=req.first_name, last_name=req.last_name, email=req.email, password=hashed_pwd,
                           role=req.role, company_id=req.company_id, address=address, updated_date=datetime.now(), updated_by=current_user.id)

    try:
        # send email with username and password
        await send_registration_email(
            password=password,
            recipient_email=new_user.email
        )
    except Exception as e:
        print(e)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(req: User, db: Session, current_user: User):
    # don't allow admin to update user to another company
    if not is_user_in_company(req.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    # don't allow USER and MODERATOR to update other users than themself
    if not user_service.is_root(current_user) and (user_service.is_user(current_user) or user_service.is_moderator(current_user)) and not user_service.is_id_same(req.id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {req.id} not found")

    #  Only ROOT can change role to ROOT
    if not user_service.is_root(current_user) and req.role == Role.ROOT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only ROOT user can change role to ROOT")

    # USER or ADMIN can't change their roles
    if (user_service.is_user(current_user) or user_service.is_moderator(current_user)) and req.role != current_user.role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not allowed to change your role")

    user = db.query(models.User).filter(models.User.id == req.id).first()

    # don't allow to update deleted user
    if user_service.is_deleted(user) or user_service.is_inactive(user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {req.id} not found")

    user_data = req.model_dump(exclude_unset=True)

    if (user.address):
        user.address = update_address(user.address, req.address, db)
    else:
        user.address = create_address(req, db)

    for key, value in user_data.items():
        setattr(user, key, value) if key != 'address' else None

    # set updated date
    user = user_service.set_updated(user, current_user)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(id: int, db: Session, current_user: User):
    user = db.query(models.User).filter(models.User.id == id).first()

    # don't allow admin to delete user from another company
    if not is_user_in_company(user.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    db.delete(user)
    db.commit()
    return {'detail': 'Successfully deleted user'}


def soft_delete_user(id: int, db: Session, current_user: User) -> User:
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    # don't allow admin to delete user from another company
    if not is_user_in_company(user.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    user.deleted = True
    # set updated date
    user = user_service.set_updated(user, current_user)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user


def change_user_status(id: int, db: Session, current_user: User) -> User:
    user = db.query(models.User).filter(models.User.id == id).first()

    # don't allow to update deleted user
    if user_service.is_deleted(user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    # don't allow admin to delete user from another company
    if not is_user_in_company(user.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    user.inactive = not user.inactive

    # set updated time
    user = user_service.set_updated(user, current_user)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user


def restore(id: int, db: Session) -> User:
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.deleted = False

    # set updated date
    user = user_service.set_updated(user, current_user)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user


def get_user(id: int, db: Session, current_user: User) -> User:
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"User with id {id} not found")

    # don't allow user to get another user data
    if user_service.is_user(current_user) and not user_service.is_id_same(id, current_user.id):
        raise not_found_exception

    user = db.query(models.User).filter(models.User.id == id).first()

    if user_service.is_root(current_user):
        return UserWithDeleted(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email, password_changed=user.password_changed, role=user.role, company_id=user.company_id, created_date=user.created_date, updated_date=user.updated_date, inactive=user.inactive, deleted=user.deleted, address=user.address)

    # don't allow to get deleted or inactive user
    if user_service.is_deleted(user) or user_service.is_inactive(user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    # check if user is in same company
    if not is_user_in_company(user.company_id, current_user) or not user:
        raise not_found_exception

    return user


def get_all_users(company_id: int, db: Session, current_user) -> List[User]:
    # don't allow admin to create user to another company
    if not is_user_in_company(company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Company id must be same like your company id")

    return db.query(models.User).filter(models.User.company_id == company_id).order_by(desc(models.User.updated_date))


def create_root(req: UserCreate, db: Session) -> User:
    hashed_pwd = hashing.Hash.bcrypt(req.password)
    new_user = models.User(first_name=req.first_name, last_name=req.last_name, email=req.email,
                           password=hashed_pwd, role=roles.Role.ROOT.value, company_id=None)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def password_change(req: PasswordChange, db: Session, current_user: UserCreate):
    # don't allow to update deleted or inactive user
    if user_service.is_deleted(current_user) or user_service.is_inactive(current_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {req.id} not found")

    if not Hash.verify(current_user.password, req.old_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')

    current_user.password = hashing.Hash.bcrypt(req.new_password)

    # set updated date
    user_service.set_updated(current_user, current_user)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {'detail': 'Password updated'}
