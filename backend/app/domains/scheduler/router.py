from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import AdminUser
from app.db.session import get_db
from app.domains.scheduler.schema import (
    SchedulerConfirmRequest,
    SchedulerResponse,
)
from app.domains.scheduler.service import SchedulerService

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
)


# =====================================
# generate
# =====================================
@router.post(
    "/generate",
    response_model=SchedulerResponse,
)
async def generate_schedule(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    result = await SchedulerService.generate(db)

    return SchedulerResponse(
        message="schedule generated",
        assignments=result,
    )


# =====================================
# confirm
# =====================================
@router.post(
    "/confirm",
    response_model=SchedulerResponse,
)
async def confirm_schedule(
    request: SchedulerConfirmRequest,
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    result = await SchedulerService.confirm(
        db=db,
        assignments=request.assignments,
    )

    return SchedulerResponse(
        message="schedule confirmed",
        assignments=result,
    )