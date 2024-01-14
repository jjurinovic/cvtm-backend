from sqlalchemy.orm import Session
from ..schemas.users import User
from .. import models, roles


def is_email_taken(email: str, db: Session) -> bool:
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return False

    return True


def is_id_same(id1: int, id2: int):
    return id1 == id2


def is_root(current_user: User) -> bool:
    return current_user.role == roles.Role.ROOT


def is_user(current_user: User) -> bool:
    return current_user.role == roles.Role.USER
