from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import get_settings

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

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session