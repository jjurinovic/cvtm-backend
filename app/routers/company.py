from fastapi import APIRouter, Depends
from .. import database, auth, roles
from sqlalchemy.orm import Session
from ..repository import company
from typing import List
from ..schemas.company import Company, CompanyCreate
from ..schemas.users import User

router = APIRouter(
    tags=['Company'],
    prefix="/company"
)


@router.post('/', response_model=Company, dependencies=[Depends(auth.RoleChecker([roles.Role.ROOT]))])
def create_company(req: CompanyCreate, db: Session = Depends(database.get_db)):
    return company.create_company(req, db)


@router.get('/{id}', response_model=Company, dependencies=[Depends(auth.RoleChecker([roles.Role.ADMIN]))])
def get_company(id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return company.get_company(id, db, current_user)


@router.get('/', response_model=List[Company], dependencies=[Depends(auth.RoleChecker([roles.Role.ROOT]))])
def get_all_companies(db: Session = Depends(database.get_db)):
    return company.get_all_companies(db)
