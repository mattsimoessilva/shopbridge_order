import asyncio
from pathlib import Path
import yaml
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from data import initialize_database
from models.entities import Order, Address, Base
from repositories import OrderRepository, AddressRepository
from services import OrderService, AddressService
from clients import ProductServiceClient, LogisticsServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

# --- Load YAML configuration ---
CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

DATABASE_PATH = Path(__file__).resolve().parent / "storage" / config.get("database_name", "database.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

APP_HOST = config.get("host", "0.0.0.0")
APP_PORT = config.get("port", 3000)
DEBUG_MODE = config.get("debug", True)

# --- Database setup ---
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

# --- App factory ---
def create_app() -> FastAPI:
    app = FastAPI(
        title="Order API",
        version="v1",
        openapi_url="/openapi.json",
        docs_url="/swagger-ui",
    )

    # Initialize repositories
    address_repository = AddressRepository(session_factory=async_session_factory)
    order_repository = OrderRepository(session_factory=async_session_factory)

    # Initialize clients
    product_client = ProductServiceClient(base_url=config.get("product_service_url", "http://localhost:5000/api/"))
    logistics_client = LogisticsServiceClient(base_url=config.get("logistics_service_url", "http://localhost:8000/api/"))

    # Initialize services
    address_service = AddressService(repository=address_repository)
    order_service = OrderService(
        repository=order_repository,
        address_repository=address_repository,
        product_client=product_client,
        logistics_client=logistics_client,
    )

    # Store shared state
    app.state.engine = engine
    app.state.session_factory = async_session_factory
    app.state.address_repository = address_repository
    app.state.order_repository = order_repository
    app.state.product_client = product_client
    app.state.logistics_client = logistics_client
    app.state.address_service = address_service
    app.state.order_service = order_service

    # Include routers
    from controllers import order_router, address_router
    app.include_router(order_router, tags=["orders"])
    app.include_router(address_router, tags=["addresses"])

    return app

app = create_app()

# --- Startup / Shutdown ---
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        address_exists = (await session.execute(select(Address))).scalars().first() is not None
        order_exists = (await session.execute(select(Order))).scalars().first() is not None
        if not address_exists and not order_exists:
            await initialize_database()

@app.on_event("shutdown")
async def shutdown_event():
    if app.state.product_client:
        await app.state.product_client.close()
    if app.state.logistics_client:
        await app.state.logistics_client.close()

# --- Run with uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=APP_HOST, port=APP_PORT, reload=DEBUG_MODE)
