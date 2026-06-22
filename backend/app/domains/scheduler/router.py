from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.core.dependencies import AdminUser

from .service import SchedulerService

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


@router.post("/generate")
async def generate_schedule(
    _: AdminUser,
    db=Depends(get_db),
):

    result = await SchedulerService.generate(db)

    return {
        "message": "schedule generated",
        "assignments": result,
    }


@router.post("/confirm")
async def confirm_schedule(
    _: AdminUser,
    db=Depends(get_db),
):

    result = await SchedulerService.confirm(db)

    return {"status": "ok", "assignments": result}