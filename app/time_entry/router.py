from fastapi import APIRouter, Depends
from typing import Optional

from .schemas import TimeEntriesDay, TimeEntry, TimeEntryCreate
from .service import TimeEntryService

TimeEntryRouter = APIRouter(
    tags=['Time Entry'],
    prefix="/time-entry",
)


@TimeEntryRouter.get('/', response_model=TimeEntriesDay)
def get_by_date(
    date: str,
    company_id: int,
    user_id: Optional[int] = None,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.list_by_date(date, company_id, user_id)


@TimeEntryRouter.post(
    '/entry',
    response_model=TimeEntry,
)
def create_time_entry(
    timeEntry: TimeEntryCreate,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.create(timeEntry)


@TimeEntryRouter.put(
    '/entry',
    response_model=TimeEntry,
)
def update_time_entry(
    timeEntry: TimeEntry,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.update(timeEntry)


@TimeEntryRouter.delete('/entry/{id}')
def delete_time_entry(id: int, timeEntryService: TimeEntryService = Depends()):
    return timeEntryService.delete(id)
