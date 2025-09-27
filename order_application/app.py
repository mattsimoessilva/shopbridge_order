import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from data import initialize_database
from models.entities import Order, Address, Base
from repositories import OrderRepository, AddressRepository
from services import OrderService, AddressService
from clients import ProductServiceClient, LogisticsServiceClient
from config import DATABASE_URL, HOST, PORT, DEBUG, PRODUCT_SERVICE_URL, LOGISTICS_SERVICE_URL

# --- Database setup ---
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

# --- Lifespan manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with ProductServiceClient(PRODUCT_SERVICE_URL) as product_client, \
               LogisticsServiceClient(LOGISTICS_SERVICE_URL) as logistics_client:

        # Initialize repositories
        address_repository = AddressRepository(session_factory=async_session_factory)
        order_repository = OrderRepository(session_factory=async_session_factory)

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

        # Run DB init
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with async_session_factory() as session:
            address_exists = (await session.execute(select(Address))).scalars().first() is not None
            order_exists = (await session.execute(select(Order))).scalars().first() is not None
            if not address_exists and not order_exists:
                await initialize_database(DATABASE_URL)

        # Yield control back to FastAPI
        yield

    # Shutdown is automatic: product_client and logistics_client exit here

# --- App factory ---
def create_app() -> FastAPI:
    app = FastAPI(
        title="Order API",
        version="v1",
        openapi_url="/openapi.json",
        docs_url="/swagger-ui",
        lifespan=lifespan,
    )

    from controllers import order_router, address_router
    app.include_router(order_router, tags=["orders"])
    app.include_router(address_router, tags=["addresses"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, reload=False)
