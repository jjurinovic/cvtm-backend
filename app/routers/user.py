from fastapi import APIRouter, Depends
from .. import database, roles, auth
from sqlalchemy.orm import Session
from ..repository import user
from typing import List
from ..schemas.users import UserCreate, User

router = APIRouter(
    tags=['users'],
    prefix="/user"
)


@router.post('/', response_model=User, dependencies=[Depends(auth.RoleChecker([roles.Role.ADMIN]))])
def create_user(req: UserCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return user.create_user(req, db, current_user)


@router.get('/{id}', response_model=User)
def get_user(id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return user.get_user(id, db, current_user)


@router.get('/', response_model=List[User], dependencies=[Depends(auth.RoleChecker([roles.Role.ADMIN, roles.Role.MODERATOR]))])
def get_all_users(company_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return user.get_all_users(company_id, db, current_user)
