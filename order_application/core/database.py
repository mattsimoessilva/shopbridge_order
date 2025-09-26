from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from config import DATABASE_URL

# --- Ensure storage directory exists ---
db_path = Path(DATABASE_URL.replace("sqlite+aiosqlite:///", ""))
db_path.parent.mkdir(parents=True, exist_ok=True)

# --- Create async engine ---
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# --- Create async session factory ---
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
