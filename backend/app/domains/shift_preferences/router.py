from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    CurrentUser,
    AdminUser,
)
from app.db.session import get_db

from app.domains.shift_preferences.schema import (
    ShiftPreferenceCreate,
    ShiftPreferenceUpdate,
    ShiftPreferenceResponse,
)

from app.domains.shift_preferences.service import (
    ShiftPreferenceService,
    ShiftPreferenceNotFoundError,
    InvalidPreferenceTimeError,
)

router = APIRouter(
    prefix="/shift-preferences",
    tags=["shift-preferences"],
)


@router.post(
    "",
    response_model=ShiftPreferenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_preference(
    preference_in: ShiftPreferenceCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftPreferenceService.create(
            db=db,
            user_id=current_user.id,  # 
            preference_in=preference_in,
        )

    except InvalidPreferenceTimeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_at must be before end_at",
        )


@router.get(
    "/me",
    response_model=list[ShiftPreferenceResponse],
)
async def get_my_preferences(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftPreferenceService.get_by_user(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[ShiftPreferenceResponse],
)
async def get_all_preferences(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftPreferenceService.get_all(db=db)


@router.get(
    "/{preference_id}",
    response_model=ShiftPreferenceResponse,
)
async def get_preference(
    preference_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftPreferenceService.get_by_id(
            db=db,
            preference_id=preference_id,
        )

    except ShiftPreferenceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found",
        )


@router.patch(
    "/{preference_id}",
    response_model=ShiftPreferenceResponse,
)
async def update_preference(
    preference_id: int,
    preference_in: ShiftPreferenceUpdate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ShiftPreferenceService.update(
            db=db,
            preference_id=preference_id,
            preference_in=preference_in,
        )

    except ShiftPreferenceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found",
        )

    except InvalidPreferenceTimeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_at must be before end_at",
        )


@router.delete(
    "/{preference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_preference(
    preference_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        await ShiftPreferenceService.delete(
            db=db,
            preference_id=preference_id,
        )

    except ShiftPreferenceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found",
        )

