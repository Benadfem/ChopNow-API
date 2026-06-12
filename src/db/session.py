from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 1. Hardcoded development connection URI string (using the asyncpg driver protocol)
DATABASE_URL = "postgresql+asyncpg://postgres:benadfem@localhost:5432/chopnow_db"

# 2. Instantiate the asynchronous DB engine with connection pooling parameters
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20
)

# 3. Create the session factory configured to manufacture async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Define the declarative base registry mapping for our database models
class Base(DeclarativeBase):
    pass

# 5. Dependency injection generator function to yield isolated requests database links
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session