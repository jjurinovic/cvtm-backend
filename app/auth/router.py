from fastapi import APIRouter, Depends
from .. import database, models
from sqlalchemy.orm import Session
from .hashing import Hash
from .token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .token import ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import LoginResponse
from .exceptions import InvalidPassword, InvalidCredentials

AuthRouter = APIRouter(
    tags=['Auth']
)


@AuthRouter.post('/login', response_model=LoginResponse)
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == req.username).first()

    # disable login if user is inactive or delete and company is inactive
    if not user or user.inactive or user.deleted or (not user.role == 0 and user.company.inactive):
        raise InvalidCredentials()

    if not Hash.verify(user.password, req.password):
        raise InvalidPassword()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "user": user}
