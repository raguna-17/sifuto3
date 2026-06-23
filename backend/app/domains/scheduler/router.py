from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.core.dependencies import AdminUser, CurrentUser
from app.domains.users.model import User

from .service import SchedulerService

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


# ==================================================
# generate (管理者のみ)
# ==================================================
@router.post("/generate")
async def generate_schedule(
    _: User = Depends(AdminUser),
    db=Depends(get_db),
):

    result = await SchedulerService.generate(db)

    return {
        "message": "schedule generated",
        "assignments": result,
    }


# ==================================================
# confirm (管理者のみ)
# ==================================================
@router.post("/confirm")
async def confirm_schedule(
    _: User = Depends(AdminUser),
    db=Depends(get_db),
):

    result = await SchedulerService.confirm(db)

    return {
        "status": "ok",
        "assignments": result,
    }