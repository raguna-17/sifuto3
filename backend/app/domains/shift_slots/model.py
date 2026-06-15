from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    func,
    Enum,
)
from app.core.enums import PositionType
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class ShiftSlot(Base):
    __tablename__ = "shift_slots"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    required_staff_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    required_position: Mapped[PositionType] = mapped_column(
        Enum(PositionType),
        nullable=False,
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

    assignments = relationship(
        "ShiftAssignment",
        back_populates="slot",
        cascade="all, delete-orphan",
    )

    preferences = relationship(
        "ShiftPreference",
        back_populates="slot",
        cascade="all, delete-orphan",
    )