from fastapi import APIRouter, Depends

from .schemas import Project, ProjectCreate, ProjectUser
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


@ProjectsRouter.get(
    '/{id}',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.MODERATOR))
    ]
)
def get_project(id: int, projectsService: ProjectsService = Depends()):
    return projectsService.get(id)


@ProjectsRouter.put(
    '/',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.MODERATOR))
    ]
)
def update_project(project: Project, projectsService: ProjectsService = Depends()):
    return projectsService.update(project)


@ProjectsRouter.post(
    '/assign-user',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.ADMIN))
    ]
)
def assign_user(req: ProjectUser, projectsService: ProjectsService = Depends()):
    return projectsService.assign_user(req.user_id, req.project_id)


@ProjectsRouter.get(
    '/user/{user_id}',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.USER))
    ]
)
def get_project(user_id: int, projectsService: ProjectsService = Depends()):
    return projectsService.getByUserId(user_id)
