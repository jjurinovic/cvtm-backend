from fastapi import Depends, HTTPException, status
from enum import Enum
from .models import User
from .auth import get_current_user


class Role(int, Enum):
    ROOT = 0
    ADMIN = 1
    MODERATOR = 2
    USER = 3


class RoleChecker:
    def __init__(self, role_required: Role):
        self.role_required = role_required

    def __call__(self, user: User = Depends(get_current_user)):
        print(type(user.role))
        print(type(self.role_required.value))
        if user.role > self.role_required.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this resource")
        return user
