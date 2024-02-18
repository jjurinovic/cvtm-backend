from sqlalchemy.orm import Session
from .. import models
from fastapi import HTTPException, status
from datetime import datetime
from ..schemas.time_entry import TimeEntriesDay, TimeEntry, TimeEntryCreate
from ..schemas.users import User
from ..services.company import is_user_in_company
from ..services.date import str_to_date, is_start_before_end
from ..services.user import is_root
from typing import Optional


def get_by_date(user_id: Optional[int], company_id: Optional[int], date: str, db: Session, current_user: User) -> TimeEntry:
    # find compy by id
    entries = db.query(models.TimeEntry).filter(models.TimeEntry.date == date)

    if (user_id):
        entries = entries.filter(models.TimeEntry.user_id == user_id).all()

    if (company_id):
        entries = entries.filter(
            models.TimeEntry.company_id == company_id).all()

    day = TimeEntriesDay(date=date, entries=entries)
    if is_root(current_user):
        return day

    return day


def create_entry(req: TimeEntryCreate, db: Session, current_user: User) -> TimeEntry:
    new_entry = models.TimeEntry(
        start_time=req.start_time, end_time=req.end_time, date=req.date, pause=req.pause, title=req.title, notes=req.notes, company_id=req.company_id, user_id=req.user_id, color=req.color)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def update_entry(req: TimeEntry, db: Session, current_user: User) -> TimeEntry:
    entry = db.query(models.TimeEntry).filter(
        models.TimeEntry.id == req.id).first()

    if not entry:
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
