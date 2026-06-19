from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class PreferencePriority(str,Enum):
    UNAVAILABLE = "unavailable"
    AVOID = "avoid"
    NEUTRAL = "neutral"
    PREFERRED = "preferred"
    REQUIRED = "required"




