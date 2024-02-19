from fastapi import Depends

from ..auth import get_current_user
from ..schemas.users import User
from ..roles import Role


def can_manipulate_self_entries(timeEntry, current_user: User = Depends(get_current_user)):
    """ if current_user.role == Role.ROOT:
        return timeEntry

    if timeEntry.user_id != current_user.id or timeEntry.company_id != current_user.company_id:
        raise  """
    return timeEntry
