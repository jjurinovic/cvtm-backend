from ..schemas.users import User
from ..roles import Role


def is_user_in_company(company_id: int, current_user: User) -> bool:
    return company_id == current_user.company_id or current_user.role == Role.ROOT
