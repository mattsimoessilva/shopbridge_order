import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from models.entities.base import Base

DATABASE_FILE = "./order.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"

async def recreate_db():
    # Remove the old DB file entirely
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(recreate_db())
