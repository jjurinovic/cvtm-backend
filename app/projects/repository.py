from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime

from .schemas import Project, ProjectCreate
from .models import Project as ProjectModel
from ..users.schemas import User
from ..auth.dependecies import get_current_user
from ..database import get_db


class ProjectsRepository:
    db: Session
    current_user: User

    def __init__(
        self,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
    ) -> None:
        self.db = db
        self.current_user = user

    # Create project
    def create(self, req: ProjectCreate) -> Project:
        project = ProjectModel(
            name=req.name,
            description=req.description,
            company_id=req.company_id,
            start_date=req.start_date,
            end_date=req.end_date,
            estimated_date=req.estimated_date,
            updated_date=datetime.now(),
            updated_by=self.current_user.id
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project
