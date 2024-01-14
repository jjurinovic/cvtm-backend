from sqlalchemy.orm import Session
from .. import models, roles
from fastapi import HTTPException, status
from datetime import datetime
from ..schemas.days import Day, DayCreate, TimeEntry
from ..schemas.users import User
from typing import List
from ..services.company import is_user_in_company
from ..services.date import str_to_date, is_start_before_end


def create_day(req: DayCreate, db: Session, current_user: User) -> Day:
    date = str_to_date(req.date)
    new_day = models.Day(
        date=date, company_id=req.company_id, user_id=req.user_id)
    db.add(new_day)
    db.commit()
    db.refresh(new_day)
    return new_day


def get_day(id: int, db: Session, current_user: User) -> Day:
    # find compy by id
    day = db.query(models.Day).filter(models.Day.id == id).first()

    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Day with id {id} not found")

    # don't allow to return company if company not belongs to admin or user is not root
    if is_user_in_company(day.company_id, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden")

    return day


def create_entry(req: TimeEntry, db: Session, current_user: User) -> TimeEntry:
    new_entry = models.TimeEntry(
        start_time=req.start_time, end_time=req.end_time, pause=req.pause, notes=req.notes, day_id=req.day_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def get_days(company_id: int, user_id: int, start: str, end: str, db: Session, current_user: User) -> List[Day]:
    start_date = datetime.strptime(start, '%Y-%m-%d').date() if start else None
    end_date = datetime.strptime(end, '%Y-%m-%d').date() if end else None

    if is_start_before_end(start_date, end_date):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Start date must be before end date")

    # get all days for given company
    days = db.query(models.Day).filter(models.Day.company_id == company_id)
    # get all days for given user
    days = days.filter(models.Day.user_id == user_id)

    # get all days after given start
    if start:
        days = days.filter(models.Day.date >= start_date)

    # get all days before given end
    if end:
        days = days.filter(models.Day.date <= end_date)

    if not days:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'not found {id}')
    return days