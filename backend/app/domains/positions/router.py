from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import AdminUser
from app.db.session import get_db

from app.domains.positions.schema import (
    PositionCreate,
    PositionUpdate,
    PositionResponse,
)

from app.domains.positions.service import (
    PositionAlreadyExistsError,
    PositionNotFoundError,
    PositionService,
)

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
)


# ==================================================
# create
# ==================================================

@router.post(
    "",
    response_model=PositionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_position(
    position_in: PositionCreate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await PositionService.create(
            db=db,
            position_in=position_in,
        )

    except PositionAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position already exists",
        )


# ==================================================
# get all
# ==================================================

@router.get(
    "",
    response_model=list[PositionResponse],
)
async def get_positions(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    return await PositionService.get_all(
        db=db,
        active_only=active_only,
    )


# ==================================================
# get by id
# ==================================================

@router.get(
    "/{position_id}",
    response_model=PositionResponse,
)
async def get_position(
    position_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await PositionService.get_by_id(
            db=db,
            position_id=position_id,
        )

    except PositionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found",
        )


# ==================================================
# update
# ==================================================

@router.patch(
    "/{position_id}",
    response_model=PositionResponse,
)
async def update_position(
    position_id: int,
    position_in: PositionUpdate,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await PositionService.update(
            db=db,
            position_id=position_id,
            position_in=position_in,
        )

    except PositionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found",
        )

    except PositionAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position already exists",
        )


# ==================================================
# deactivate
# ==================================================

@router.delete(
    "/{position_id}",
    response_model=PositionResponse,
)
async def deactivate_position(
    position_id: int,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await PositionService.deactivate(
            db=db,
            position_id=position_id,
        )

    except PositionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found",
        )

