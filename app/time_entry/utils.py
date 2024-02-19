from .schemas import TimeEntry
from ..users.schemas import User
from ..roles import Role


def can_manipulate_time_entry(timeEntry: TimeEntry, current_user: User) -> bool:
    if current_user.role == Role.ROOT:
        return True

    if timeEntry.user_id != current_user.id or timeEntry.company_id != current_user.company_id:
        return False

    return True
