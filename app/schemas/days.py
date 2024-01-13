from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import date, time


class TimeEntryCreate(BaseModel):
    start_time: time
    end_time: time
    pause: int
    notes: str
    day_id: int


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
