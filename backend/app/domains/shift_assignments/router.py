from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser, AdminUser
from app.db.session import get_db

from app.domains.shift_assignments.schema import (
    ShiftAssignmentCreate,
    ShiftAssignmentUpdate,
    ShiftAssignmentResponse,
)

from app.domains.shift_assignments.service import (
    ShiftAssignmentService,
    ShiftAssignmentNotFoundError,
    DuplicateAssignmentError,
    AssignmentCapacityError,
    ShiftSlotNotFoundError,
    UserNotFoundError,
)

router = APIRouter(
    prefix="/shift-assignments",
    tags=["shift-assignments"],
)

# =========================
# create (USER)
# =========================
@router.post("", response_model=ShiftAssignmentResponse)
async def create_assignment(
    assignment_in: ShiftAssignmentCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftAssignmentService.create(
            db=db,
            user_id=current_user.id,
            slot_id=assignment_in.slot_id,
            is_auto=True,
        )

    except (ShiftSlotNotFoundError, UserNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Slot not found",
        )

    except DuplicateAssignmentError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate assignment",
        )

    except AssignmentCapacityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot capacity exceeded",
        )


# =========================
# bulk create (ADMIN ONLY)
# =========================
@router.post("/bulk/{user_id}")
async def bulk_create(
    user_id: int,
    payload: list[ShiftAssignmentCreate],
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftAssignmentService.bulk_create(
            db=db,
            user_id=user_id,
            slot_ids=[p.slot_id for p in payload],
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =========================
# get all (ADMIN ONLY)
# =========================
@router.get("", response_model=list[ShiftAssignmentResponse])
async def get_all_assignments(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftAssignmentService.get_all(db)


# =========================
# get my assignments
# =========================
@router.get("/me", response_model=list[ShiftAssignmentResponse])
async def get_my_assignments(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftAssignmentService.get_by_user(
        db=db,
        user_id=current_user.id,
    )


# =========================
# get by id (ADMIN ONLY)
# =========================
@router.get("/{assignment_id}", response_model=ShiftAssignmentResponse)
async def get_assignment(
    assignment_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftAssignmentService.get_by_id(
            db=db,
            assignment_id=assignment_id,
        )
    except ShiftAssignmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )


# =========================
# update (ADMIN ONLY)
# =========================
@router.patch("/{assignment_id}", response_model=ShiftAssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_in: ShiftAssignmentUpdate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftAssignmentService.update(
            db=db,
            assignment_id=assignment_id,
            assignment_in=assignment_in,
        )
    except ShiftAssignmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )


# =========================
# delete (ADMIN ONLY)
# =========================
@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        await ShiftAssignmentService.delete(
            db=db,
            assignment_id=assignment_id,
        )
    except ShiftAssignmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )