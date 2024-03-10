from fastapi import APIRouter, Depends
from typing import Optional, List

from .schemas import Project, ProjectCreate, ProjectUsers, ProjectInfo
from .service import ProjectsService
from ..roles import RoleChecker, Role
from ..pagination import PagedResponse, PageParams, PageFilter

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
    '/list',
    response_model=PagedResponse[Project],
    dependencies=[Depends(RoleChecker(Role.MODERATOR))]
)
def get_all_users(
    company_id: Optional[int] = None,
    page_params: PageParams = Depends(PageParams),
    projectsService: ProjectsService = Depends()
):
    return projectsService.get_all(company_id, page_params)


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
    '/assign-users',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.ADMIN))
    ]
)
def assign_users(req: ProjectUsers, projectsService: ProjectsService = Depends()):
    return projectsService.assign_users(req)


@ProjectsRouter.post(
    '/remove-users',
    response_model=Project,
    dependencies=[
        Depends(RoleChecker(Role.ADMIN))
    ]
)
def remove_users(req: ProjectUsers, projectsService: ProjectsService = Depends()):
    return projectsService.remove_users(req)


@ProjectsRouter.get(
    '/user/{user_id}',
    response_model=List[ProjectInfo],
    dependencies=[
        Depends(RoleChecker(Role.USER))
    ]
)
def get_project(user_id: int, projectsService: ProjectsService = Depends()):
    return projectsService.getByUserId(user_id)
