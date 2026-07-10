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
from app.core.enums import UserRole
from app.db.session import get_db

from app.domains.shift_preferences.schema import (
    ShiftPreferenceCreate,
    ShiftPreferenceUpdate,
    ShiftPreferenceResponse,
)

from app.domains.shift_preferences.service import (
    ShiftPreferenceService,
    ShiftPreferenceNotFoundError,
)

router = APIRouter(
    prefix="/shift-preferences",
    tags=["shift-preferences"],
)


# ==================================================
# create (LOGIN REQUIRED)
# ==================================================
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
    return await ShiftPreferenceService.create(
        db=db,
        user_id=current_user.id,
        preference_in=preference_in,
    )


# ==================================================
# get my preferences (LOGIN REQUIRED)
# ==================================================
@router.get(
    "/me",
    response_model=list[ShiftPreferenceResponse],
)
async def get_my_preferences(
    shift_slot_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftPreferenceService.get_by_user(
        db=db,
        user_id=current_user.id,
        shift_slot_id=shift_slot_id,
    )


# ==================================================
# get all (ADMIN ONLY)
# ==================================================
@router.get(
    "",
    response_model=list[ShiftPreferenceResponse],
)
async def get_all_preferences(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    return await ShiftPreferenceService.get_all(db=db)


# ==================================================
# get by id (ADMIN ONLY)
# ==================================================
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


# ==================================================
# update (OWNER or ADMIN)
# ==================================================
@router.patch(
    "/{preference_id}",
    response_model=ShiftPreferenceResponse,
)
async def update_preference(
    preference_id: int,
    preference_in: ShiftPreferenceUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        pref = await ShiftPreferenceService.get_by_id(
            db=db,
            preference_id=preference_id,
        )

        # owner or admin only
        if pref.user_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="not allowed",
            )

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


# ==================================================
# delete (OWNER or ADMIN)
# ==================================================
@router.delete(
    "/{preference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_preference(
    preference_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        pref = await ShiftPreferenceService.get_by_id(
            db=db,
            preference_id=preference_id,
        )

        if pref.user_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="not allowed",
            )

        await ShiftPreferenceService.delete(
            db=db,
            preference_id=preference_id,
        )

    except ShiftPreferenceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found",
        )