import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models.entities.base import Base

DATABASE_URL = "sqlite+aiosqlite:///./order.db"

async def recreate_db():
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(recreate_db())
