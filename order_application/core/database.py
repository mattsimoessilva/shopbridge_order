# core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./order_application/data/database.db"

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL, echo=True, future=True
)

# Create async session factory
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
