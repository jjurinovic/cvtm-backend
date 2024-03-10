from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

from ..users.schemas import UserInfo


class ProjectCreate(BaseModel):
    start_date: date
    end_date: Optional[date] = None
    estimated_date: Optional[date] = None
    company_id: int
    name: str
    description: Optional[str] = None


class ProjectInfo(ProjectCreate):
    id: int
    active: bool


class Project(ProjectInfo):
    users: List[UserInfo] = []
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config():
        from_attributes = True


class ProjectUsers(BaseModel):
    project_id: int
    users: List[int] = []
