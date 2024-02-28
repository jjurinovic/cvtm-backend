from fastapi import Depends
from typing import List

from .repository import ProjectsRepository
from .schemas import ProjectCreate, Project
from .exceptions import ProjectNotFound, UserAlreadyAssigned

from ..auth.dependecies import get_current_user
from ..users.schemas import User, UserInfo
from ..company.utils import is_user_in_company
from ..company.service import CompanyService
from ..users.exceptions import NotSameCompany, UserNotFound
from ..users.service import UsersService


class ProjectsService:
    projectsRepository: ProjectsRepository
    companyService: CompanyService
    usersService: UsersService
    current_user: User

    def __init__(
        self,
        user: User = Depends(get_current_user),
        projectsRepository: ProjectsRepository = Depends(),
        companyService: CompanyService = Depends(),
        usersService: UsersService = Depends()
    ) -> None:
        self.projectsRepository = projectsRepository
        self.companyService = companyService
        self.usersService = usersService
        self.current_user = user

    # Create project
    def create(self, req: ProjectCreate) -> Project:
        # not allowed to create project for another company
        if not is_user_in_company(req.company_id, self.current_user):
            raise NotSameCompany()

        # check if company exists
        self.companyService.get(req.company_id)

        return self.projectsRepository.create(req)

    # Get project
    def get(self, id: int) -> Project:
        project = self.projectsRepository.get(id)

        if not project or not is_user_in_company(project.company_id, self.current_user):
            raise ProjectNotFound()

        return project

    # Update project
    def update(self, req: Project) -> Project:
        project = self.projectsRepository.get(req.id)

        if not project or not is_user_in_company(project.company_id, self.current_user):
            raise ProjectNotFound()

        return self.projectsRepository.update(req, project)

    def assign_user(self, user_id: int, project_id: int) -> Project:
        # get project
        project = self.get(project_id)
        # get user
        user = self.usersService.get_by_id(user_id, True)

        if user in project.users:
            raise UserAlreadyAssigned()

        self.projectsRepository.assign_user(user, project)

        return self.get(project.id)

    def getByUserId(self, user_id: int) -> List[Project]:
        # call get user to check if user exits
        user = self.usersService.get_by_id(user_id)

        return self.projectsRepository.get_all(user_id)
