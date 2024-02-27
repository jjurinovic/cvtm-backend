from fastapi import Depends

from .repository import ProjectsRepository
from .schemas import ProjectCreate, Project

from ..auth.dependecies import get_current_user
from ..users.schemas import User
from ..company.utils import is_user_in_company
from ..company.repository import CompanyRepository
from ..company.exceptions import CompanyNotFound
from ..users.exceptions import NotSameCompany


class ProjectsService:
    projectsRepository: ProjectsRepository
    companyRepository: CompanyRepository
    current_user: User

    def __init__(
        self,
        user: User = Depends(get_current_user),
        projectsRepository: ProjectsRepository = Depends(),
        companyRepository: CompanyRepository = Depends()
    ) -> None:
        self.projectsRepository = projectsRepository
        self.companyRepository = companyRepository
        self.current_user = user

    def create(self, req: ProjectCreate) -> Project:
        # not allowed to create project for another company
        if not is_user_in_company(req.company_id, self.current_user):
            raise NotSameCompany()

        # check if company exists
        if not self.companyRepository.get(req.company_id):
            raise CompanyNotFound()

        return self.projectsRepository.create(req)
