from fastapi import APIRouter, Depends
from .. import schemas, database, auth, roles
from sqlalchemy.orm import Session
from ..repository import company
from typing import List

router = APIRouter(
    tags=['Company'],
    prefix="/company"
)


@router.post('/', response_model=schemas.ShowCompany, dependencies=[Depends(auth.RoleChecker([roles.Role.ROOT]))])
def create_company(req: schemas.Company, db: Session = Depends(database.get_db)):
    return company.create_company(req, db)


@router.get('/{id}', response_model=schemas.ShowCompany)
def get_company(id: int, db: Session = Depends(database.get_db)):
    return company.get_company(id, db)


@router.get('/', response_model=List[schemas.ShowCompany], dependencies=[Depends(auth.RoleChecker([roles.Role.ROOT]))])
def get_all_companies(db: Session = Depends(database.get_db)):
    return company.get_all_companies(db)
