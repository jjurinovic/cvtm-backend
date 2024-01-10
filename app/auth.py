from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token, models, database, roles
from typing import List
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = token.verify(data, credentials_exception)
    if token_data:
        user = db.query(models.User).filter(
            token_data.username == models.User.email).first()
        if user is None:
            raise credentials_exception
        return user


class RoleChecker:
    def __init__(self, permissions_required: List[roles.Role]):
        self.permissions_required = permissions_required

    def __call__(self, user: models.User = Depends(get_current_user)):
        if user.role == roles.Role.ROOT:
            return user

        if user.role not in self.permissions_required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this resource")
        return user