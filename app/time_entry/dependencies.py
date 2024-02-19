from fastapi import Depends

from ..auth.dependecies import get_current_user
from ..users.schemas import User
from ..roles import Role
from .exceptions import TimeEntryNotFound
from .utils import can_manipulate_time_entry


def can_manipulate_self_entries(timeEntry, current_user: User = Depends(get_current_user)):
    if not can_manipulate_time_entry(timeEntry, current_user):
        raise TimeEntryNotFound()

    return timeEntry
