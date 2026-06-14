from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(settings.DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    """Dependency for providing a database session to handlers."""
    async with async_session() as session:
        yield session
        await session.commit()