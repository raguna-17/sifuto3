from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.db.session import get_db

from app.domains.users.schema import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)

from app.domains.users.service import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError,
    UserService,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# ==================================================
# register
# ==================================================

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


# ==================================================
# login
# ==================================================

@router.post(
    "/login",
    response_model=Token,
)
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await UserService.login(
            db=db,
            email=user_in.email,
            password=user_in.password,
        )

    except UserInactiveError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


# ==================================================
# current user
# ==================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: CurrentUser,
):
    return current_user

