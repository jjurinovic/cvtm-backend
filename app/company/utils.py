from datetime import datetime

from .schemas import Company
from ..users.schemas import User
from ..users.utils import is_root


def set_updated(company: Company, user: User) -> Company:
    company.updated_date = datetime.now()
    company.updated_by = user.id
    return user


def is_user_in_company(company_id: int, current_user: User) -> bool:
    return is_root(current_user.role) or company_id == current_user.company_id
