from fastapi import APIRouter, Depends
from .. import schemas, database, auth, roles
from sqlalchemy.orm import Session
from ..repository import day
from typing import List

router = APIRouter(
    tags=['Days'],
    prefix="/day"
)


@router.post('/', response_model=schemas.Day, dependencies=[Depends(auth.RoleChecker([roles.Role.ADMIN, roles.Role.MODERATOR, roles.Role.USER]))])
def create_day(req: schemas.Day, db: Session = Depends(database.get_db)):
    return day.create_day(req, db)
