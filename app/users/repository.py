from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List

from ..email.send_email import send_registration_email
from ..database import get_db
from .utils import create_random_password, set_updated
from .. import models
from .schemas import User, UserCreate, UserWithDeleted, PasswordChange
from ..address.repository import AddressRepository
from ..auth.hashing import Hash
from ..roles import Role


class UsersRepository:
    db: Session
    addressRepository: AddressRepository

    def __init__(
        self,
        db: Session = Depends(get_db),
        addressRepository: AddressRepository = Depends()
    ) -> None:
        self.db = db
        self.addressRepository = addressRepository

    # Create user
    async def create(self, user: UserCreate) -> User:

        address = None
        if (user.address):
            address = self.addressRepository.create(user.address)

        # create random password
        password = create_random_password()
        hashed_password = Hash.bcrypt(password)

        new_user = models.User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            role=user.role,
            company_id=user.company_id,
            address=address,
            updated_date=datetime.now(),
            updated_by=self.current_user.id
        )

        try:
            # send email with username and password
            await send_registration_email(
                password=password,
                recipient_email=new_user.email
            )
        except Exception as e:
            print(e)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    # Get user by email
    def get_by_email(self, email: str) -> User:
        user = self.db.query(models.User).filter(
            models.User.email == email).first()

        return user

    # Get user by id
    def get_by_id(self, id: int) -> UserWithDeleted:
        user = self.db.query(models.User).filter(
            models.User.id == id).first()

        return user

    # Update user
    def update(self, req: User, user: User) -> User:
        user_data = req.model_dump(exclude_unset=True)

        if not user.address:
            user.address = AddressRepository.create(req.address)
        else:
            user.address = AddressRepository.update(req.address)

        for key, value in user_data.items():
            setattr(user, key, value) if key != 'address' else None

        # set updated date
        user = set_updated(user, self.current_user)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Delete user
    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()
        return {'detail': 'Successfully deleted user'}

    # Soft delete user
    def soft_delete(self, user: UserWithDeleted) -> UserWithDeleted:
        user.deleted = True

        # set updated date
        user = set_updated(user, self.current_user)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Change user status
    def change_status(self, user: User) -> User:
        user.inactive = not user.inactive

        # set updated date
        user = set_updated(user, self.current_user)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Restore deleted user
    def restore(self, user: UserWithDeleted) -> UserWithDeleted:
        user.deleted = False

        # set updated date
        user = set_updated(user, self.current_user)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Get all users
    def get_all(self, company_id: int) -> List[UserWithDeleted]:
        return self.db.query(models.User).filter(models.User.company_id ==
                                                 company_id)

    # Create root user
    async def create_root(self, req: UserCreate) -> User:
        # create random password
        password = create_random_password()
        hashed_password = Hash.bcrypt(password)

        new_user = models.User(
            first_name=req.first_name,
            last_name=req.last_name,
            email=req.email,
            password=hashed_password,
            role=Role.ROOT.value,
            company_id=None
        )

        try:
            # send email with username and password
            await send_registration_email(
                password=password,
                recipient_email=new_user.email
            )
        except Exception as e:
            print(e)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    # Password change
    def password_change(self, req: PasswordChange):
        self.current_user.password = Hash.bcrypt(req.new_password)

        # set updated date
        set_updated(self.current_user, self.current_user)

        self.db.add(self.current_user)
        self.db.commit()
        self.db.refresh(self.current_user)
        return {'detail': 'Password updated'}
