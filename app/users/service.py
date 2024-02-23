from fastapi import Depends
from typing import Union

from .repository import UsersRepository
from .schemas import User, UserCreate, PasswordChange, UserWithDeleted
from .utils import is_root, is_deleted_or_inactive, is_user, is_moderator
from .exceptions import OnlyRootCanCreateRoot, EmailAlreadyTaken, UserNotFound, InvalidPassword, NotSameCompany, NotAllowedRoleChange

from ..auth.dependecies import get_current_user
from ..auth.hashing import Hash
from ..schemas import PageParams, PagedResponse
from ..pagination import filter
from .. import models
from ..company.utils import is_user_in_company


class UsersService:
    usersRepository: UsersRepository
    current_user: User

    def __init__(
        self,
        user: User = Depends(get_current_user),
        usersRepository: UsersRepository = Depends()
    ) -> None:
        self.usersRepository = usersRepository
        self.current_user = user

    # Create user
    async def create(self, user: UserCreate) -> User:
        # only ROOT can create ROOT user
        if is_root(user.role) and is_root(self.current_user.role):
            raise OnlyRootCanCreateRoot()

        # check if email is taken
        if self.get_by_email(user.email):
            raise EmailAlreadyTaken()

        if not is_root(self.current_user) and not is_user_in_company(user.company_id, self.current_user):
            raise NotSameCompany()

        return self.usersRepository.create(user)

    # Get user by email
    def get_by_email(self, email: str) -> User:
        user = self.usersRepository.get_by_email(email)

        if not user:
            raise UserNotFound()

        return user

    # Get user by id
    def get_by_id(self, id: int) -> Union[User, UserWithDeleted]:
        user = self.usersRepository.get_by_id(id)

        if is_root(self.current_user.role):
            return UserWithDeleted(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password_changed=user.password_changed,
                role=user.role,
                company_id=user.company_id,
                created_date=user.created_date,
                updated_date=user.updated_date,
                inactive=user.inactive,
                deleted=user.deleted,
                address=user.address
            )

        if not user or is_deleted_or_inactive(user) or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return user

    # Update user
    def update(self, req: User) -> User:
        user = self.usersRepository.get_by_id(req.id)

        # only ROOT can update to ROOT user
        if is_root(user.role) and is_root(self.current_user.role):
            raise OnlyRootCanCreateRoot()

        # USER or ADMIN can't change their roles
        if (is_user(self.current_user.role) or is_moderator(self.current_user.role)) and req.role != self.current_user.role:
            raise NotAllowedRoleChange()

        user_mod_other_update = (is_user(self.current_user.role) or is_moderator(
            self.current_user.role)) and req.id != self.current_user.id

        if not user or is_deleted_or_inactive(user) or user_mod_other_update or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.update(req, user)

    # Delete user
    def delete(self, id: int):
        user = self.usersRepository.get_by_id(id)

        if not user or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.delete(user)

    # Soft delete
    def soft_delete(self, id: int):
        user = self.usersRepository.get_by_id(id)

        if not user or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.soft_delete(user)

    # Change status
    def change_status(self, id: int):
        user = self.usersRepository.get_by_id(id)

        if not user or user.deleted or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.change_status(user)

    # Restore
    def restore(self, id: int) -> UserWithDeleted:
        user = self.usersRepository.get_by_id(id)

        if not user:
            raise UserNotFound()

        return self.usersRepository.restore(user)

    # Get all users by company id
    def get_all(self, company_id: int, page_params: PageParams) -> PagedResponse[UserWithDeleted]:
        # user have to be in same company or root
        if not is_user_in_company(company_id, self.current_user):
            raise NotSameCompany()

        query = self.usersRepository.get_all(company_id)

        return filter(page_params, query, UserWithDeleted, models.User, ['first_name', 'last_name'])

    # Create root user
    async def create_root(self, req: UserCreate) -> User:
        # check if email is taken
        if self.get_by_email(req.email):
            raise EmailAlreadyTaken()

        return await self.usersRepository.create_root(req)

    # Password change
    def password_change(self, req: PasswordChange):
        if self.current_user.deleted or self.current_user.inactive:
            raise UserNotFound()

        if not Hash.verify(self.current_user.password, req.old_password):
            raise InvalidPassword()

        return self.usersRepository.password_change(req)
