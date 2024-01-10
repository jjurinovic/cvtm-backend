from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    tags=['users'],
    prefix="/user"
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(req: schemas.User, db: Session = Depends(database.get_db)):
    return user.create_user(req, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.get_user(id, db)
