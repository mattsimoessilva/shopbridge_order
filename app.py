import asyncio
from flask import Flask, g
from flask_smorest import Api
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from data.db_initializer import initialize_database
from controllers import order_blp as OrderController, address_blp as AddressController
from models.entities.order import Order
from models.entities.address import Address
from repositories.order_repository_impl import OrderRepository
from repositories.address_repository_impl import AddressRepository
from services.order_service_impl import OrderService
from services.address_service_impl import AddressService
from models.entities.base import Base
from clients.product_service_client import ProductServiceClient
from clients.logistics_service_client import LogisticsServiceClient


DATABASE_URL = "sqlite+aiosqlite:///./order.db"


def create_app():
    app = Flask(__name__)

    app.config.update(
        API_TITLE="Order API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/",
        OPENAPI_SWAGGER_UI_PATH="/swagger-ui",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        OPENAPI_JSON_PATH="openapi.json"
    )

    api = Api(app)

    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    address_repository = AddressRepository(session_factory=async_session_factory)
    order_repository = OrderRepository(session_factory=async_session_factory)

    product_client = ProductServiceClient(base_url="http://localhost:5000/api/")
    logistics_client = LogisticsServiceClient(base_url="http://localhost:8000/api/")

    address_service = AddressService(repository=address_repository)
    order_service = OrderService(
        repository=order_repository,
        address_repository=address_repository,
        product_client=product_client,
        logistics_client=logistics_client
    )

    app.extensions.update(
        engine=engine,
        session_factory=async_session_factory,
        address_repository=address_repository,
        order_repository=order_repository,
        product_client=product_client,
        logistics_client=logistics_client,
        address_service=address_service,
        order_service=order_service
    )

    @app.before_request
    async def create_session():
        g.db = async_session_factory()

    @app.teardown_request
    async def close_session(exc):
        session = getattr(g, "db", None)
        if session is not None:
            try:
                await session.close()
            except Exception:
                pass

    api.register_blueprint(OrderController)
    api.register_blueprint(AddressController)

    return app


async def startup(app):
    engine = app.extensions["engine"]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_factory = app.extensions["session_factory"]

    async with async_session_factory() as session:
        address_exists = (await session.execute(select(Address))).scalars().first() is not None
        order_exists = (await session.execute(select(Order))).scalars().first() is not None

        if not address_exists and not order_exists:
            await initialize_database()

    product_client = ProductServiceClient(base_url="http://localhost:5000/api/")
    logistics_client = LogisticsServiceClient(base_url="http://localhost:8000/api/")

    address_service = AddressService(repository=app.extensions["address_repository"])
    order_service = OrderService(
        repository=app.extensions["order_repository"],
        address_repository=app.extensions["address_repository"],
        product_client=product_client,
        logistics_client=logistics_client
    )

    app.extensions.update(
        product_client=product_client,
        logistics_client=logistics_client,
        address_service=address_service,
        order_service=order_service
    )


async def shutdown(app):
    await app.extensions["product_client"].close()
    await app.extensions["logistics_client"].close()


app = create_app()


if __name__ == "__main__":
    try:
        from hypercorn.asyncio import serve
        from hypercorn.config import Config

        config = Config()
        config.bind = ["0.0.0.0:3000"]

        asyncio.run(startup(app))

        try:
            asyncio.run(serve(app, config))
        finally:
            asyncio.run(shutdown(app))

    except ImportError:
        print("Hypercorn not installed. Falling back to Flask dev server.")

        asyncio.run(startup(app))

        try:
            app.run(debug=True)
        finally:
            asyncio.run(shutdown(app))
