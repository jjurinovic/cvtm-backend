from fastapi import Depends

from .repository import UsersRepository
from .schemas import User, UserCreate, PasswordChange
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

    async def create(self, user: UserCreate) -> User:
        # only ROOT can create ROOT user
        if is_root(user.role) and is_root(self.current_user.role):
            raise OnlyRootCanCreateRoot()

        # check if email is taken
        if self.get_by_email(user.email):
            raise EmailAlreadyTaken()

        return self.usersRepository.create(user)

    def get_by_email(self, email: str) -> User:
        user = self.usersRepository.get_by_email(email)

        if not user:
            raise UserNotFound()

        return user

    def get_by_id(self, id: int) -> User:
        user = self.usersRepository.get_by_id(id)

        if not user or is_deleted_or_inactive(user):
            raise UserNotFound()

        return user

    def update(self, req: User) -> User:
        user = self.get_by_id(req.id)

        # only ROOT can update to ROOT user
        if is_root(user.role) and is_root(self.current_user.role):
            raise OnlyRootCanCreateRoot()

        # USER or ADMIN can't change their roles
        if (is_user(self.current_user) or is_moderator(self.current_user)) and req.role != self.current_user.role:
            raise NotAllowedRoleChange()

        user_mod_other_update = (is_user(self.current_user) or is_moderator(
            self.current_user)) and req.id != self.current_user.id

        if not user or is_deleted_or_inactive(user) or user_mod_other_update:
            raise UserNotFound()

        return self.usersRepository.update(req, user)

    # Delete user
    def delete(self, id: int):
        user = self.get_by_id(id)

        if not user or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.delete(user)

    # Soft delete
    def soft_delete(self, id: int):
        user = self.get_by_id(id)

        if not user or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.soft_delete(user)

    # Change status
    def change_status(self, id: int):
        user = self.get_by_id(id)

        if not user or user.deleted or not is_user_in_company(user.company_id, self.current_user):
            raise UserNotFound()

        return self.usersRepository.soft_delete(user)

    # Restore
    def restore(self, id: int) -> User:
        user = self.get_by_id(id)

        if not user:
            raise UserNotFound()

        return self.usersRepository.restore(user)

    # Get all users by company id
    def get_all(self, company_id: int, page_params: PageParams) -> PagedResponse[User]:
        # user have to be in same company or root
        if not is_user_in_company(company_id, self.current_user):
            raise NotSameCompany()

        query = self.usersRepository.get_all(company_id)

        return filter(page_params, query, User, models.User, ['first_name', 'last_name'])

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
