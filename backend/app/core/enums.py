from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class PreferencePriority(str,Enum):
    UNAVAILABLE = "unavailable"
    AVOID = "avoid"
    NEUTRAL = "neutral"
    PREFERRED = "preferred"
    REQUIRED = "required"


class ShiftStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


