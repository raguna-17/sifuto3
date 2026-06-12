from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ShiftSlotRequirement(Base):
    __tablename__ = "shift_slot_requirements"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("shift_slots.id"),
        nullable=False,
    )

    position_id: Mapped[int] = mapped_column(
        ForeignKey("positions.id"),
        nullable=False,
    )

    required_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )



    slot = relationship(
        "ShiftSlot",
        back_populates="requirements",
    )

    position = relationship(
        "Position",
    )

