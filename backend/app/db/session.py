from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from app.core.config import get_settings


settings = get_settings()

DATABASE_URL = settings.DATABASE_URL


def create_engine_by_env():
    if settings.ENV == "test":
        return create_async_engine(
            DATABASE_URL,
            echo=settings.DEBUG,
            poolclass=NullPool,
        )

    return create_async_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=1800,
    )


engine = create_engine_by_env()


SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session