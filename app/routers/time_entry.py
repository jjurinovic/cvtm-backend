from fastapi import APIRouter, Depends
from .. import database, auth
from ..schemas.time_entry import TimeEntriesDay, TimeEntry, TimeEntryCreate
from ..schemas.users import User
from sqlalchemy.orm import Session
from ..repository import time_entry
from typing import Optional

router = APIRouter(
    tags=['Time Entries'],
    prefix="/time-entries"
)


@router.get('/', response_model=TimeEntriesDay)
def get_by_date(date: str, user_id: Optional[int] = None, company_id: Optional[int] = None, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return time_entry.get_by_date(user_id, company_id, date, db, current_user)


@router.post('/entry', response_model=TimeEntry)
def create_entry(req: TimeEntryCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return time_entry.create_entry(req, db, current_user)


@router.put('/entry', response_model=TimeEntry)
def update_entry(req: TimeEntry, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return time_entry.update_entry(req, db, current_user)
