from fastapi import APIRouter, Depends
from .. import database, roles, auth
from sqlalchemy.orm import Session
from ..repository import user
from ..schemas.users import UserCreate, User, PasswordChange, UserWithCompany, UserWithDeleted
from ..schemas.pagination import PagedResponse, PageParams
from ..pagination import filter
from ..models import User as UserModel
from ..email.send_email import send_registration_email
from typing import Union

router = APIRouter(
    tags=['Users'],
    prefix="/user"
)


@router.post('/', response_model=User, dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))])
async def create_user(req: UserCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return await user.create_user(req, db, current_user)


@router.put('/', response_model=User)
def update_user(req: User, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return user.update_user(req, db, current_user)


@router.delete('/{id}', dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))])
def delete_user(id: int, db: Session = Depends(database.get_db), current_user: UserWithCompany = Depends(auth.get_current_user)):
    return user.delete_user(id, db, current_user)


@router.delete('/{id}/soft', dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))])
def soft_delete_user(id: int, db: Session = Depends(database.get_db), current_user: UserWithCompany = Depends(auth.get_current_user)):
    return user.soft_delete_user(id, db, current_user)


@router.put('/{id}/status-change', response_model=UserWithDeleted, dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))])
def change_user_status(id: int, db: Session = Depends(database.get_db), current_user: UserWithCompany = Depends(auth.get_current_user)):
    return user.change_user_status(id, db, current_user)


@router.put('/{id}/restore', response_model=UserWithDeleted, dependencies=[Depends(roles.RoleChecker(roles.Role.ROOT))])
def restore_user(id: int, db: Session = Depends(database.get_db), current_user: UserWithCompany = Depends(auth.get_current_user)):
    return user.restore(id, db)


@router.post('/root', response_model=User)
def create_root_user(req: UserCreate, db: Session = Depends(database.get_db)):
    return user.create_root(req, db)


@router.get('/me', response_model=UserWithCompany)
def get_current_user(current_user: UserWithCompany = Depends(auth.get_current_user)):
    return current_user


@router.get('/{id}', response_model=Union[User, UserWithDeleted])
def get_user(id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return user.get_user(id, db, current_user)


@router.get('/', response_model=PagedResponse[UserWithDeleted], dependencies=[Depends(roles.RoleChecker(roles.Role.MODERATOR))])
def get_all_users(company_id: int, page_params: PageParams = Depends(PageParams), db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    query = user.get_all_users(company_id, db, current_user)
    return filter(page_params, query, UserWithDeleted, UserModel, ['first_name', 'last_name', 'email'])


@router.put('/change-password')
def change_password(req: PasswordChange, db: Session = Depends(database.get_db), current_user: UserCreate = Depends(auth.get_current_user)):
    return user.password_change(req, db, current_user)
