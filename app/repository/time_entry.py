from sqlalchemy.orm import Session
from .. import models, database
from fastapi import HTTPException, status, Depends
from ..schemas.time_entry import TimeEntriesDay, TimeEntry, TimeEntryCreate
from ..schemas.users import User
from ..services.company import is_user_in_company
from ..services.user import is_root, is_id_same, is_user
from typing import Optional
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
        user_id: Optional[int],
        company_id: Optional[int]
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
        if is_root(self.current_user):
            return day

        return day

    def create(
        self,
        time_entry: TimeEntryCreate
    ) -> TimeEntry:
        """ if (not is_id_same(time_entry.user_id, current_user.id) or
                not is_user_in_company(time_entry.company_id, current_user)) and not is_root(current_user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"You are not allowed to create Time Entry for another users") """

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


def update_entry(req: TimeEntry, db: Session, current_user: User) -> TimeEntry:
    entry = db.query(models.TimeEntry).filter(
        models.TimeEntry.id == req.id).first()

    if not is_root(current_user) and (not entry or not (is_user(current_user) and
                                                        is_id_same(entry.user_id, current_user.id))):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Entry with id {req.id} not found")

    entry_data = req.model_dump(exclude_unset=True)

    for key, value in entry_data.items():
        setattr(entry, key, value) if key not in [
            'day_id', 'date', 'user_id'] else None

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def delete_entry(id: int, db: Session, current_user: User):
    entry = db.query(models.TimeEntry).filter(
        models.TimeEntry.id == id).one_or_none()

    # if not enrty or user company is not same like from entry
    if not is_root(current_user) and (not entry or not is_user_in_company(entry.company_id, current_user) or
                                      not (is_user(current_user) and is_id_same(entry.user_id, current_user.id))):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Entry with id {id} not found")

    db.delete(entry)
    db.commit()
    return {"detail": "Successfully deleted Time entry"}
