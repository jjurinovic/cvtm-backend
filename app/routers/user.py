from fastapi import APIRouter, Depends
from .. import schemas, database, roles, auth
from sqlalchemy.orm import Session
from ..repository import user
from typing import List

router = APIRouter(
    tags=['users'],
    prefix="/user"
)


@router.post('/', response_model=schemas.ShowUser, dependencies=[Depends(auth.RoleChecker([roles.Role.ADMIN]))])
def create_user(req: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return user.create_user(req, db, current_user)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return user.get_user(id, db, current_user)


@router.get('/', response_model=List[schemas.ShowUser], dependencies=[Depends(auth.RoleChecker([roles.Role.ADMIN, roles.Role.MODERATOR]))])
def get_all_users(company_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return user.get_all_users(company_id, db, current_user)
