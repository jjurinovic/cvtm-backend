import string
import secrets
from datetime import datetime

from ..roles import Role
from .schemas import UserWithDeleted, User


def create_random_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    return password


def is_root(role: Role):
    return role == Role.ROOT


def is_admin(role: Role):
    return role == Role.ADMIN


def is_moderator(role: Role):
    return role == Role.MODERATOR


def is_user(role: Role):
    return role == Role.USER


def is_deleted(user: UserWithDeleted):
    return user.deleted


def set_updated(user: User, current_user: User):
    user.updated_date = datetime.now()
    user.updated_by = current_user.id
    return user
