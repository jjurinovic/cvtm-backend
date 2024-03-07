from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime
from typing import Optional, List

from .schemas import Project, ProjectCreate
from .models import Project as ProjectModel, project_users
from .utils import set_updated

from ..users.schemas import User, UserInfo
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

    # Get project
    def get(self, id: int) -> Project:
        project = self.db.query(ProjectModel).filter(
            ProjectModel.id == id).first()

        return project

    # Update project
    def update(self, req: Project, project: Project) -> Project:
        project_data = req.model_dump(exclude_unset=True)

        for key, value in project_data.items():
            setattr(project, key, value) if key != 'users' else None

        # set updated date
        project = set_updated(project, self.current_user)

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    # Assign users to project
    def assign_users(self, users: List[User], project: Project) -> Project:
        for user in users:
            project.users.append(user)

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    # Remove users from project
    def remove_users(self, users: List[User], project: Project) -> Project:
        for user in users:
            project.users.remove(user)

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    # Get all projects by user or company
    def get_all(self, company_id: int) -> List[Project]:
        projects = self.db.query(ProjectModel).filter(
            ProjectModel.company_id == company_id)
        return projects

    # Get all project from user
    def get_by_user(self, user: User) -> List[Project]:
        pass
