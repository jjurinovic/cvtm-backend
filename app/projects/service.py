from fastapi import Depends
from typing import List, Optional

from .repository import ProjectsRepository
from .schemas import ProjectCreate, Project, ProjectUsers
from .exceptions import ProjectNotFound, UserAlreadyAssigned
from .models import Project as ProjectModel

from ..auth.dependecies import get_current_user
from ..users.schemas import User
from ..company.utils import is_user_in_company
from ..company.service import CompanyService
from ..users.exceptions import NotSameCompany
from ..users.service import UsersService
from ..pagination import PageParams, PagedResponse, filter


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

    # Assign users to project
    def assign_users(self, req: ProjectUsers) -> Project:
        # get project
        project = self.get(req.project_id)

        users = []
        for user_id in req.users:
            # get users
            user = self.usersService.get_by_id(user_id, True)

            if user in project.users:
                raise UserAlreadyAssigned()

            users.append(user)

        self.projectsRepository.assign_users(users, project)

        return self.get(project.id)

    # Remove users from project
    def remove_users(self, req: ProjectUsers) -> Project:
        # get project
        project = self.get(req.project_id)

        users = []
        for user_id in req.users:
            # get users
            user = self.usersService.get_by_id(user_id, True)

            if user in project.users:
                users.append(user)

        self.projectsRepository.remove_users(users, project)

        return self.get(project.id)

    # Get user by id
    def getByUserId(self, user_id: int) -> List[Project]:
        # call get user to check if user exits
        user = self.usersService.get_by_id(user_id)

        return self.projectsRepository.get_by_user(user)

    # Get all projects by company id
    def get_all(self, company_id: Optional[int], page_params: PageParams) -> PagedResponse[Project]:
        if not company_id:
            company_id = self.current_user.company_id

        # user have to be in same company or root
        if not is_user_in_company(company_id, self.current_user):
            raise NotSameCompany()

        query = self.projectsRepository.get_all(company_id)

        return filter(page_params, query, Project, ProjectModel, ['name'])
