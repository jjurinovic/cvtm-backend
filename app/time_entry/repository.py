from fastapi import Depends
from typing import Optional
from sqlalchemy.orm import Session

from .. import models, database
from .schemas import TimeEntriesDay, TimeEntry, TimeEntryCreate
from ..users.schemas import User
from ..users.utils import is_root
from ..auth.dependecies import get_current_user


class TimeEntryRepository:
    db: Session
    current_user: User

    def __init__(
        self,
        db: Session = Depends(database.get_db),
        user: User = Depends(get_current_user)
    ) -> None:
        self.db = db
        self.current_user = user

    def list_by_date(
        self,
        date: str,
        company_id: int,
        user_id: Optional[int],
    ) -> TimeEntriesDay:
        # find by date
        entries = self.db.query(models.TimeEntry).filter(
            models.TimeEntry.date == date)

        if user_id:
            entries = entries.filter(models.TimeEntry.user_id == user_id).all()

        if company_id:
            entries = entries.filter(
                models.TimeEntry.company_id == company_id).all()

        day = TimeEntriesDay(date=date, entries=entries)
        if is_root(self.current_user.role):
            return day

        return day

    def create(
        self,
        time_entry: TimeEntryCreate
    ) -> TimeEntry:
        new_entry = models.TimeEntry(
            start_time=time_entry.start_time,
            end_time=time_entry.end_time,
            date=time_entry.date,
            pause=time_entry.pause,
            title=time_entry.title,
            notes=time_entry.notes,
            company_id=time_entry.company_id,
            user_id=time_entry.user_id,
            color=time_entry.color
        )
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)
        return new_entry

    def update(self, req: TimeEntry, entry: TimeEntry) -> TimeEntry:
        entry_data = req.model_dump(exclude_unset=True)

        for key, value in entry_data.items():
            setattr(entry, key, value) if key not in [
                'date', 'user_id', 'company_id'] else None

        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_by_id(self, id: int) -> TimeEntry:
        return self.db.query(models.TimeEntry).filter(models.TimeEntry.id == id).one_or_none()

    def delete(self, timeEntry: TimeEntry):
        self.db.delete(timeEntry)
        self.db.commit()
        return {"detail": "Successfully deleted Time entry"}
