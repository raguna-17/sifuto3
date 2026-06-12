from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    AdminUser,
)
from app.db.session import get_db

from app.domains.shift_slot_requirements.schema import (
    ShiftSlotRequirementCreate,
    ShiftSlotRequirementUpdate,
    ShiftSlotRequirementResponse,
)

from app.domains.shift_slot_requirements.service import (
    PositionNotFoundError,
    RequirementNotFoundError,
    ShiftSlotNotFoundError,
    ShiftSlotRequirementService,
)

router = APIRouter(
    prefix="/shift-slot-requirements",
    tags=["shift-slot-requirements"],
)


@router.post(
    "/slots/{slot_id}",
    response_model=ShiftSlotRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_requirement(
    slot_id: int,
    requirement_in: ShiftSlotRequirementCreate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await (
            ShiftSlotRequirementService
            .create(
                db=db,
                slot_id=slot_id,
                position_id=requirement_in.position_id,
                required_count=requirement_in.required_count,
            )
        )

    except ShiftSlotNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Shift slot not found",
        )

    except PositionNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Position not found",
        )


@router.get(
    "/slots/{slot_id}",
    response_model=list[
        ShiftSlotRequirementResponse
    ],
)
async def get_requirements(
    slot_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await (
        ShiftSlotRequirementService
        .get_by_slot(
            db=db,
            slot_id=slot_id,
        )
    )


@router.patch(
    "/{requirement_id}",
    response_model=ShiftSlotRequirementResponse,
)
async def update_requirement(
    requirement_id: int,
    requirement_in: ShiftSlotRequirementUpdate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await (
            ShiftSlotRequirementService
            .update(
                db=db,
                requirement_id=requirement_id,
                required_count=requirement_in.required_count,
            )
        )

    except RequirementNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found",
        )


@router.delete(
    "/{requirement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_requirement(
    requirement_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        await (
            ShiftSlotRequirementService
            .delete(
                db=db,
                requirement_id=requirement_id,
            )
        )

    except RequirementNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found",
        )
