from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.core.enums import ShiftStatus


class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"

    # =========================
    # identity
    # =========================
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # =========================
    # relations
    # =========================
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("shift_slots.id"),
        nullable=False,
        index=True,
    )

    # =========================
    # metadata
    # =========================
    is_auto: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    status: Mapped[ShiftStatus] = mapped_column(
        Enum(ShiftStatus, name="shift_status"),
        nullable=False,
        default=ShiftStatus.CONFIRMED,
    )

    # =========================
    # timestamps
    # =========================
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

    # =========================
    # constraints（重要）
    # =========================
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "slot_id",
            name="uq_user_slot_assignment",
        ),
    )

    # =========================
    # relationships
    # =========================
    user = relationship(
        "User",
        back_populates="assignments",
    )

    slot = relationship(
        "ShiftSlot",
        back_populates="assignments",
    )