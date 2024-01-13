from sqlalchemy.orm import Session
from .. import models, schemas, roles
from fastapi import HTTPException, status
from datetime import datetime


def str_to_date(val: str):
    return datetime.strptime(val, '%Y-%m-%d').date()


def create_day(req: schemas.Day, db: Session, current_user: schemas.User):
    date = str_to_date(req.date)
    new_day = models.Day(
        date=date, company_id=req.company_id, user_id=req.user_id)
    db.add(new_day)
    db.commit()
    db.refresh(new_day)
    return new_day


def get_day(id: int, db: Session, current_user: schemas.User):
    # find compy by id
    day = db.query(models.Day).filter(models.Day.id == id).first()

    if not day:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Day with id {id} not found")

    # don't allow to return company if company not belongs to admin or user is not root
    if day.company_id != current_user.company_id and current_user.role != roles.Role.ROOT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden")

    return day


def create_entry(req: schemas.TimeEntry, db: Session, current_user: schemas.User):
    new_entry = models.TimeEntry(
        start_time=req.start_time, end_time=req.end_time, pause=req.pause, notes=req.notes, day_id=req.day_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def get_days(company_id: int, user_id: int, start, end, db):
    # get all days for given company
    days = db.query(models.Day).filter(models.Day.company_id == company_id)
    # get all days for given user
    days = days.filter(models.Day.user_id == user_id)

    # get all days after given start
    if start:
        s = datetime.strptime(start, '%Y-%m-%d').date()
        days = days.filter(models.Day.date >= s)

    # get all days before given end
    if end:
        e = datetime.strptime(end, '%Y-%m-%d').date()
        days = days.filter(models.Day.date <= e)

    if not days:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'not found {id}')
    return days
