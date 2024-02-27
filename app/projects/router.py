from fastapi import APIRouter, Depends

from .schemas import Project, ProjectCreate
from .service import ProjectsService
from ..roles import RoleChecker, Role

ProjectsRouter = APIRouter(
    tags=['Projects'],
    prefix="/project"
)


@ProjectsRouter.post(
    '/',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.ADMIN))
    ]
)
def create_project(req: ProjectCreate, projectsService: ProjectsService = Depends()):
    return projectsService.create(req)
