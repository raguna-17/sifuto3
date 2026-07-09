from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import AdminUser, CurrentUser
from app.db.session import get_db
from app.domains.shift_assignments.schema import (
    ShiftAssignmentResponse,
    ShiftAssignmentUpdate,
)
from app.domains.shift_assignments.service import (
    ShiftAssignmentNotFoundError,
    ShiftAssignmentService,
)

router = APIRouter(
    prefix="/shift-assignments",
    tags=["shift-assignments"],
)


# =========================
# get all (ADMIN)
# =========================
@router.get(
    "",
    response_model=list[ShiftAssignmentResponse],
)
async def get_all_assignments(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftAssignmentService.get_all(db)


# =========================
# get my assignments
# =========================
@router.get(
    "/me",
    response_model=list[ShiftAssignmentResponse],
)
async def get_my_assignments(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftAssignmentService.get_by_user(
        db=db,
        user_id=current_user.id,
    )


# =========================
# get by id (ADMIN)
# =========================
@router.get(
    "/{assignment_id}",
    response_model=ShiftAssignmentResponse,
)
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
# update (ADMIN)
# =========================
@router.patch(
    "/{assignment_id}",
    response_model=ShiftAssignmentResponse,
)
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
# delete (ADMIN)
# =========================
@router.delete(
    "/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
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