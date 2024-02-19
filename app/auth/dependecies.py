from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from . import token
from .. import models, database
from sqlalchemy.orm import Session
from .exceptions import NoValidCredentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = token.verify(data)
    if token_data:
        user = db.query(models.User).filter(
            token_data.username == models.User.email).first()
        if user is None:
            raise NoValidCredentials()
        return user
