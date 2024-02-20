from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Union

from .schemas import UserCreate, User, PasswordChange, UserWithCompany, UserWithDeleted
from .service import UsersService

from .. import roles
from ..pagination import PagedResponse, PageParams
from ..auth.dependecies import get_current_user

UsersRouter = APIRouter(
    tags=['Users'],
    prefix="/user"
)


@UsersRouter.post(
    '/',
    response_model=User,
    dependencies=[
        Depends(roles.RoleChecker(
            roles.Role.ADMIN))
    ]
)
async def create_user(req: UserCreate, usersService: UsersService = Depends()):
    return await usersService.create(req)


@UsersRouter.put(
    '/',
    response_model=User,
    dependencies=[
        Depends(roles.RoleChecker(
            roles.Role.ADMIN))
    ]
)
def update_user(req: User, usersService: UsersService = Depends()):
    print(req)
    return usersService.update(req)


@UsersRouter.delete(
    '/{id}',
    dependencies=[Depends(roles.RoleChecker(roles.Role.ROOT))]
)
def delete_user(id: int,  usersService: UsersService = Depends()):
    return usersService.delete(id)


@UsersRouter.delete(
    '/{id}/soft',
    dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))]
)
def soft_delete_user(id: int, usersService: UsersService = Depends()):
    return usersService.soft_delete(id)


@UsersRouter.put(
    '/{id}/status-change',
    response_model=UserWithDeleted,
    dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))]
)
def change_user_status(id: int, usersService: UsersService = Depends()):
    return usersService.change_status(id)


@UsersRouter.put(
    '/{id}/restore',
    response_model=UserWithDeleted,
    dependencies=[Depends(roles.RoleChecker(roles.Role.ROOT))]
)
def restore_user(id: int, usersService: UsersService = Depends()):
    return usersService.restore(id)


@UsersRouter.post('/root', response_model=User)
def create_root_user(req: UserCreate, usersService: UsersService = Depends()):
    return usersService.create_root(req)


@UsersRouter.get('/me', response_model=UserWithCompany)
def get_current_user(current_user: UserWithCompany = Depends(get_current_user)):
    return current_user


@UsersRouter.get('/{id}', response_model=Union[User, UserWithDeleted])
def get_user(id: int, usersService: UsersService = Depends()):
    return usersService.get_by_id(id)


@UsersRouter.get(
    '/',
    response_model=PagedResponse[UserWithDeleted],
    dependencies=[Depends(roles.RoleChecker(roles.Role.MODERATOR))]
)
def get_all_users(
    company_id: int,
    page_params: PageParams = Depends(PageParams),
    usersService: UsersService = Depends()
):
    return usersService.get_all(company_id, page_params)


@UsersRouter.put('/change-password')
def change_password(req: PasswordChange, usersService: UsersService = Depends()):
    return usersService.password_change(req)
