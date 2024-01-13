from fastapi import APIRouter, Depends, status
from .. import schemas, database, auth, roles
from sqlalchemy.orm import Session
from ..repository import day
from typing import List
from datetime import date

router = APIRouter(
    tags=['Days'],
    prefix="/day"
)


@router.post('/', response_model=schemas.ShowDay)
def create_day(req: schemas.Day, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    new_day = day.create_day(req, db, current_user)
    return new_day


@router.get('/{id}', response_model=schemas.ShowDay)
def get_day(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return day.get_day(id, db, current_user)


@router.post('/entry', response_model=schemas.TimeEntry)
def create_entry(req: schemas.TimeEntry, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return day.create_entry(req, db, current_user)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowDay])
def get_days(company_id: int, user_id: int, start: str, end: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return day.get_days(company_id, user_id, start, end, db)
