from datetime import datetime

from .schemas import Project
from ..users.schemas import User


def set_updated(project: Project, user: User) -> Project:
    project.updated_by = user.id
    project.updated_date = datetime.now()

    return project
