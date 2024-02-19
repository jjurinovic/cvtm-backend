from fastapi import APIRouter, Depends
from .. import database
from ..schemas.time_entry import TimeEntriesDay, TimeEntry, TimeEntryCreate
from ..schemas.users import User
from sqlalchemy.orm import Session
from ..repository import time_entry
from typing import Optional
from ..services.time_entry import TimeEntryService
from ..dependecies.time_entry import can_manipulate_self_entries
from ..auth.dependecies import get_current_user

TimeEntryRouter = APIRouter(
    tags=['Time Entry'],
    prefix="/time-entry",
)


@TimeEntryRouter.get('/', response_model=TimeEntriesDay)
def get_by_date(
    date: str,
    user_id: Optional[int] = None,
    company_id: Optional[int] = None,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.list_by_date(date, user_id, company_id)


@TimeEntryRouter.post(
    '/entry',
    response_model=TimeEntry,
    dependencies=[Depends(can_manipulate_self_entries)]
)
def create_entry(
    timeEntry: TimeEntryCreate,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.create(timeEntry)


@TimeEntryRouter.put('/entry', response_model=TimeEntry)
def update_entry(req: TimeEntry, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return time_entry.update_entry(req, db, current_user)


@TimeEntryRouter.delete('/entry/{id}')
def delete_entry(id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return time_entry.delete_entry(id, db, current_user)
