from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from .service import CompanyService
from .schemas import Company, CompanyCreate

from ..roles import Role, RoleChecker
from ..schemas import PagedResponse, PageParams


CompanyRouter = APIRouter(
    tags=['Company'],
    prefix="/company"
)


@CompanyRouter.post(
    '/',
    response_model=Company,
    dependencies=[Depends(RoleChecker(Role.ROOT))]
)
def create_company(
    req: CompanyCreate,
    companyService: CompanyService = Depends()
):
    return companyService.create(req)


@CompanyRouter.get(
    '/{id}',
    response_model=Company,
    dependencies=[Depends(RoleChecker(Role.ADMIN))]
)
def get_company(id: int, companyService: CompanyService = Depends()):
    return companyService.get(id)


@CompanyRouter.put(
    '/',
    response_model=Company,
    dependencies=[Depends(RoleChecker(Role.ADMIN))]
)
def update_company(req: Company, companyService: CompanyService = Depends()):
    return companyService.update(req)


@CompanyRouter.get(
    '/',
    response_model=PagedResponse[Company],
    dependencies=[Depends(RoleChecker(Role.ROOT))]
)
def get_all_companies(
    page_params: PageParams = Depends(PageParams),
    companyService: CompanyService = Depends()
):
    return companyService.get_all(page_params)


@CompanyRouter.delete(
    '/{id}',
    dependencies=[Depends(RoleChecker(Role.ROOT))]
)
def delete_company(id: int, companyService: CompanyService = Depends()):
    return companyService.delete(id)


@CompanyRouter.put(
    '/{id}/status-change',
    response_model=Company,
    dependencies=[Depends(RoleChecker(Role.ROOT))]
)
def change_company_status(id: int, companyService: CompanyService = Depends()):
    return companyService.change_status(id)
