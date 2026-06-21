from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser,AdminUser
from app.db.session import get_db

from app.domains.users.schema import (
    LoginRequest,
    Token,
    UserCreate,
    UserResponse,
)

from app.domains.users.service import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserService,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# ==========================================
# Register
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await UserService.create_user(
            db=db,
            user_in=user_in,
        )

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )


# ==========================================
# Login
# ==========================================

@router.post(
    "/login",
    response_model=Token,
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await UserService.login(
            db=db,
            email=login_data.email,
            password=login_data.password,
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


# ==========================================
# Current User
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: CurrentUser,
):
    return current_user


@router.get("")
async def get_users(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.get_all(db)