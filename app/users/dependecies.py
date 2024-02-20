
from fastapi import Depends

from ..auth.dependecies import get_current_user
from .schemas import User
from .utils import is_root
from .exceptions import NotSameCompany


def is_in_company(user, current_user: User = Depends(get_current_user)):
    if not is_root(current_user.role) and user.company_id != current_user.company_id:
        raise NotSameCompany()

    return user
