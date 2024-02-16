from fastapi import APIRouter, Depends, status
from .. import database, auth
from ..schemas.days import Day, DayCreate, TimeEntry, TimeEntryCreate
from ..schemas.users import User
from sqlalchemy.orm import Session
from ..repository import day
from typing import List, Optional

router = APIRouter(
    tags=['Days'],
    prefix="/day"
)


@router.post('/', response_model=Day)
def create_day(req: DayCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    new_day = day.create_day(req, db, current_user)
    return new_day


@router.get('/', response_model=Day)
def get_day(user_id: int, date: str, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return day.get_day(user_id, date, db, current_user)


@router.post('/entry', response_model=TimeEntry)
def create_entry(req: TimeEntryCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return day.create_entry(req, db, current_user)


@router.put('/entry', response_model=TimeEntry)
def update_entry(req: TimeEntry, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return day.update_entry(req, db, current_user)


@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[Day])
def get_days(company_id: int, user_id: int, start: Optional[str] = None, end: Optional[str] = None, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return day.get_days(company_id, user_id, start, end, db, current_user)
