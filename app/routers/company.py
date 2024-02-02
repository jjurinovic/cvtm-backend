from fastapi import APIRouter, Depends
from .. import database, auth, roles
from sqlalchemy.orm import Session
from ..repository import company
from typing import List
from ..schemas.company import Company, CompanyCreate
from ..schemas.users import User
from ..schemas.pagination import PagedResponse, PageParams
from ..pagination import filter
from ..models import Company as c

router = APIRouter(
    tags=['Company'],
    prefix="/company"
)


@router.post('/', response_model=Company, dependencies=[Depends(roles.RoleChecker(roles.Role.ROOT))])
def create_company(req: CompanyCreate, db: Session = Depends(database.get_db)):
    return company.create_company(req, db)


@router.get('/{id}', response_model=Company, dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))])
def get_company(id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return company.get_company(id, db, current_user)


@router.put('/', response_model=Company, dependencies=[Depends(roles.RoleChecker(roles.Role.ADMIN))])
def update_company(req: Company, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return company.update_company(req, db, current_user)


@router.get('/', response_model=PagedResponse[Company], dependencies=[Depends(roles.RoleChecker(roles.Role.ROOT))])
def get_all_companies(page_params: PageParams = Depends(PageParams), db: Session = Depends(database.get_db)):
    query = company.get_all_companies(db)
    return filter(page_params, query, Company, c, ['name', 'vat'])
