from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Import your validated settings manager object
from src.db.config import db_settings

# 1. Instantiate the non-blocking engine using your secure configuration url
engine = create_async_engine(
    db_settings.ASYNC_DATABASE_URL,  # No hardcoded strings or passwords!
    echo=False,
    pool_size=10,
    max_overflow=20
)

# 2. Create the session factory configured to manufacture async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Define the declarative base registry mapping for our database models
class Base(DeclarativeBase):
    pass

# 4. Dependency injection generator function to yield isolated requests database links
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session