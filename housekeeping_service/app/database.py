"""Database initialization and session handling for async SQLAlchemy."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Async engine using the DB_URL from settings.
engine = create_async_engine(settings.DB_URL, echo=False, future=True)

# Async session factory.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db() -> AsyncSession:
    """FastAPI dependency that provides a transactional DB session.

    Usage in path operations:
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
