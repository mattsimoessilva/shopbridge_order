from pathlib import Path
import yaml
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# --- Load configuration ---
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

database_name = config.get("database_name", "database.db")
DATABASE_PATH = Path(__file__).resolve().parent.parent / "storage" / database_name
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# --- Create async engine ---
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# --- Create async session factory ---
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
