import asyncio
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from data.db_initializer import initialize_database
from models.entities.order import Order
from models.entities.address import Address
from models.entities.base import Base
from repositories.order_repository_impl import OrderRepository
from repositories.address_repository_impl import AddressRepository
from services.order_service_impl import OrderService
from services.address_service_impl import AddressService
from clients.product_service_client import ProductServiceClient
from clients.logistics_service_client import LogisticsServiceClient

DATABASE_URL = "sqlite+aiosqlite:///./order.db"

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
        docs_url="/swagger-ui",  # FastAPI already ships Swagger UI
    )

    # Initialize repositories
    address_repository = AddressRepository(session_factory=async_session_factory)
    order_repository = OrderRepository(session_factory=async_session_factory)

    # Initialize clients (not yet opened)
    product_client = ProductServiceClient(base_url="http://localhost:5000/api/")
    logistics_client = LogisticsServiceClient(base_url="http://localhost:8000/api/")

    # Initialize services
    address_service = AddressService(repository=address_repository)
    order_service = OrderService(
        repository=order_repository,
        address_repository=address_repository,
        product_client=product_client,
        logistics_client=logistics_client,
    )

    # Store shared state in app
    app.state.engine = engine
    app.state.session_factory = async_session_factory
    app.state.address_repository = address_repository
    app.state.order_repository = order_repository
    app.state.product_client = product_client
    app.state.logistics_client = logistics_client
    app.state.address_service = address_service
    app.state.order_service = order_service

    # Import and include your routers instead of Flask blueprints
    from controllers import order_router, address_router
    app.include_router(order_router, prefix="/api/orders", tags=["orders"])
    app.include_router(address_router, prefix="/api/addresses", tags=["addresses"])

    return app

app = create_app()

# --- Startup / Shutdown ---
@app.on_event("startup")
async def startup_event():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed DB if empty
    async with async_session_factory() as session:
        address_exists = (await session.execute(select(Address))).scalars().first() is not None
        order_exists = (await session.execute(select(Order))).scalars().first() is not None
        if not address_exists and not order_exists:
            await initialize_database()

    # Open async clients
    app.state.product_client = await ProductServiceClient("http://localhost:5000/api/").open()
    app.state.logistics_client = await LogisticsServiceClient("http://localhost:8000/api/").open()

    # Re-init services with opened clients
    app.state.address_service = AddressService(repository=app.state.address_repository)
    app.state.order_service = OrderService(
        repository=app.state.order_repository,
        address_repository=app.state.address_repository,
        product_client=app.state.product_client,
        logistics_client=app.state.logistics_client,
    )

@app.on_event("shutdown")
async def shutdown_event():
    if app.state.product_client:
        await app.state.product_client.close()
    if app.state.logistics_client:
        await app.state.logistics_client.close()

# --- Run with uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)
