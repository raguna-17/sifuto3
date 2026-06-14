from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    String,
    Boolean,
    ForeignKey,
    Table,
    Column,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.enums import UserRole


# ==================================================
# ser Position
# ==================================================
user_positions = Table(
    "user_positions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("position_id", ForeignKey("positions.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.USER,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ==================================================
    # relationships
    # ==================================================

    preferences = relationship(
        "ShiftPreference",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    assignments = relationship(
        "ShiftAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    positions = relationship(
        "Position",
        secondary=user_positions,
        back_populates="users",
    )

