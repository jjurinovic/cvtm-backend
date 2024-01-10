from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"
    ROOT = "ROOT"
