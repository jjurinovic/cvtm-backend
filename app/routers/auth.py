from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES
from ..schemas.auth import LoginResponse
from ..services.user import is_inactive, is_deleted


router = APIRouter(
    tags=['Auth']
)


@router.post('/login', response_model=LoginResponse)
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == req.username).first()

    if not user or is_inactive(user) or is_deleted(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    if not Hash.verify(user.password, req.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "user": user}
