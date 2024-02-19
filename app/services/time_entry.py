from fastapi import Depends
from typing import Optional

from ..repository.time_entry import TimeEntryRepository
from ..schemas.time_entry import TimeEntry, TimeEntriesDay, TimeEntryCreate


class TimeEntryService:
    timeEntryRepository: TimeEntryRepository

    def __init__(
        self,
        timeEntryRepository: TimeEntryRepository = Depends()
    ) -> None:
        self.timeEntryRepository = timeEntryRepository

    def list_by_date(
        self,
        date: str,
        user_id: Optional[int],
        company_id: Optional[int]
    ) -> TimeEntriesDay:
        return self.timeEntryRepository.list_by_date(
            date, user_id, company_id
        )

    def create(
        self,
        timeEntry: TimeEntryCreate
    ) -> TimeEntry:
        return self.timeEntryRepository.create(timeEntry)
