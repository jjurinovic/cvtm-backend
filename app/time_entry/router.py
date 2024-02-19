from fastapi import APIRouter, Depends
from typing import Optional

from .schemas import TimeEntriesDay, TimeEntry, TimeEntryCreate
from .service import TimeEntryService
from .dependencies import can_manipulate_self_entries

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
    return timeEntryService.list_by_date(date, user_id, company_id)


@TimeEntryRouter.post(
    '/entry',
    response_model=TimeEntry,
    dependencies=[Depends(can_manipulate_self_entries)]
)
def create_time_entry(
    timeEntry: TimeEntryCreate,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.create(timeEntry)


@TimeEntryRouter.put(
    '/entry',
    response_model=TimeEntry,
    dependencies=[Depends(can_manipulate_self_entries)]
)
def update_time_entry(
    timeEntry: TimeEntry,
    timeEntryService: TimeEntryService = Depends()
):
    return timeEntryService.update(timeEntry)


@TimeEntryRouter.delete('/entry/{id}')
def delete_time_entry(id: int, timeEntryService: TimeEntryService = Depends()):
    return timeEntryService.delete(id)
