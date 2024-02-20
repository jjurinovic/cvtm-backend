from fastapi import Depends
from typing import Optional

from .repository import TimeEntryRepository
from .schemas import TimeEntry, TimeEntriesDay, TimeEntryCreate
from .exceptions import TimeEntryNotFound, NotAllowedTimeEntries
from .utils import can_manipulate_time_entry

from ..users.schemas import User
from ..auth.dependecies import get_current_user
from ..users.exceptions import NotSameCompany
from ..users.utils import is_root, is_user


class TimeEntryService:
    timeEntryRepository: TimeEntryRepository
    current_user: User

    def __init__(
        self,
        timeEntryRepository: TimeEntryRepository = Depends(),
        user: User = Depends(get_current_user)
    ) -> None:
        self.timeEntryRepository = timeEntryRepository
        self.current_user = user

    def list_by_date(
        self,
        date: str,
        company_id: int,
        user_id: Optional[int],
    ) -> TimeEntriesDay:
        if not is_root(self.current_user.role) and company_id != self.current_user.company_id:
            raise NotSameCompany()

        if is_user(self.current_user.role) and user_id != self.current_user.id:
            raise NotAllowedTimeEntries()

        return self.timeEntryRepository.list_by_date(
            date, company_id, user_id
        )

    def create(
        self,
        timeEntry: TimeEntryCreate
    ) -> TimeEntry:
        # if entry doens't exist or can't manipulate, raise exception
        if not can_manipulate_time_entry(timeEntry, self.current_user):
            raise TimeEntryNotFound()

        return self.timeEntryRepository.create(timeEntry)

    def update(
        self,
        timeEntry: TimeEntry
    ) -> TimeEntry:
        entry = self.timeEntryRepository.get_by_id(timeEntry.id)

        # if entry doens't exist or can't manipulate, raise exception
        if not entry or not can_manipulate_time_entry(entry, self.current_user):
            raise TimeEntryNotFound()

        return self.timeEntryRepository.update(timeEntry, entry)

    def delete(
        self,
        id: int
    ):
        entry = self.timeEntryRepository.get_by_id(id)

        # if entry doens't exist or can't manipulate, raise exception
        if not entry or not can_manipulate_time_entry(entry, self.current_user):
            raise TimeEntryNotFound()

        return self.timeEntryRepository.delete(entry)
