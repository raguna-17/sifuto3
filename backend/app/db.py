from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from app.core.config import get_settings

Base = declarative_base()

engine = None
async_session = None


def init_db():
    """
    DB初期化（遅延実行）
    import時には絶対呼ばれない
    """
    global engine, async_session

    settings = get_settings()

    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=(settings.ENV == "dev"),
        pool_pre_ping=True,
    )

    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


def get_session_maker():
    """
    session factory取得（安全）
    """
    if async_session is None:
        init_db()

    return async_session


async def get_db():
    """
    FastAPI dependency用
    """
    session_maker = get_session_maker()

    async with session_maker()() as session:
        yield session