from pydantic import BaseModel, field_validator, computed_field
from typing import List
from typing import Optional
from datetime import date, time, timedelta


class TimeEntryCreate(BaseModel):
    day_id: int
    start_time: time
    end_time: time
    pause: Optional[int] = None
    notes: Optional[str] = None
    date: date
    title: str
    user_id: int
    color: Optional[str] = None


class TimeEntry(TimeEntryCreate):
    id: int
    total: int = 0

    @field_validator("total", mode="before")
    @classmethod
    def transform(cls, raw: timedelta) -> int:
        return raw.seconds


class DayCreate(BaseModel):
    date: str
    user_id: int
    company_id: int


class Day(DayCreate):
    id: int
    date: date
    entries: List[TimeEntry]

    @computed_field
    @property
    def total(self) -> int:
        return sum(entry.total for entry in self.entries)
