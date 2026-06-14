from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import AdminUser
from app.db.session import get_db

from app.domains.shift_slots.schema import (
    ShiftSlotCreate,
    ShiftSlotUpdate,
    ShiftSlotResponse,
)

from app.domains.shift_slots.service import (
    ShiftSlotService,
    ShiftSlotNotFoundError,
    InvalidShiftTimeError,
)

router = APIRouter(
    prefix="/shift-slots",
    tags=["shift-slots"],
)


# ==================================================
# create
# ==================================================

@router.post(
    "",
    response_model=ShiftSlotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shift_slot(
    slot_in: ShiftSlotCreate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftSlotService.create(
            db=db,
            slot_in=slot_in,
        )

    except InvalidShiftTimeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_at must be before end_at",
        )


# ==================================================
# get all
# ==================================================

@router.get(
    "",
    response_model=list[ShiftSlotResponse],
)
async def get_shift_slots(
    db: AsyncSession = Depends(get_db),
):
    return await ShiftSlotService.get_all(db)


# ==================================================
# get by id
# ==================================================

@router.get(
    "/{slot_id}",
    response_model=ShiftSlotResponse,
)
async def get_shift_slot(
    slot_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftSlotService.get_by_id(
            db=db,
            slot_id=slot_id,
        )

    except ShiftSlotNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift slot not found",
        )


# ==================================================
# update
# ==================================================

@router.patch(
    "/{slot_id}",
    response_model=ShiftSlotResponse,
)
async def update_shift_slot(
    slot_id: int,
    slot_in: ShiftSlotUpdate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftSlotService.update(
            db=db,
            slot_id=slot_id,
            slot_in=slot_in,
        )

    except ShiftSlotNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift slot not found",
        )

    except InvalidShiftTimeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_at must be before end_at",
        )


# ==================================================
# delete
# ==================================================

@router.delete(
    "/{slot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_shift_slot(
    slot_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        await ShiftSlotService.delete(
            db=db,
            slot_id=slot_id,
        )

    except ShiftSlotNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift slot not found",
        )

