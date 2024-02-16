from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import date, time


class TimeEntryCreate(BaseModel):
    day_id: int
    start_time: time
    end_time: time
    pause: Optional[int] = None
    notes: Optional[str] = None
    date: date
    title: str
    user_id: int


class TimeEntry(TimeEntryCreate):
    id: int


class DayCreate(BaseModel):
    date: str
    user_id: int
    company_id: int


class Day(DayCreate):
    id: int
    date: date
    entries: List[TimeEntry]
