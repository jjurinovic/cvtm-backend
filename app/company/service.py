from fastapi import Depends

from .repository import CompanyRepository
from .schemas import Company, CompanyCreate
from .exceptions import CompanyNotFound
from .utils import is_user_in_company

from .. import models
from ..auth.dependecies import get_current_user
from ..users.schemas import User
from ..users.utils import is_root
from ..pagination import filter
from ..schemas import PagedResponse, PageParams


class CompanyService:
    companyRepository: CompanyRepository
    current_user: User

    def __init__(
        self,
        companyRepository: CompanyRepository = Depends(),
        user: User = Depends(get_current_user)
    ) -> None:
        self.companyRepository = companyRepository
        self.current_user = user

    # Create company
    def create(self, req: CompanyCreate) -> Company:
        return self.companyRepository.create(req)

    # Get company by id
    def get(self, id: int) -> Company:
        if not is_user_in_company(id, self.current_user):
            raise CompanyNotFound()
        return self.companyRepository.get(id)

    # Get all companies
    def get_all(self, page_params: PageParams) -> PagedResponse[Company]:
        query = self.companyRepository.get_all()
        return filter(page_params, query, Company, models.Company, ['name', 'vat'])

    # Update company
    def update(self, req: Company) -> Company:
        company = self.get(req.id)

        if not is_user_in_company(id, self.current_user) or not company:
            raise CompanyNotFound()

        return self.companyRepository.update(req, company)

    # Delete company
    def delete(self, id: int):
        company = self.get(id)

        if not company:
            raise CompanyNotFound()

        return self.companyRepository.delete(company)

    # Change status
    def change_status(self, id: int) -> Company:
        company = self.companyRepository.get(id)

        if not company:
            raise CompanyNotFound()

        return self.companyRepository.change_status(company)
