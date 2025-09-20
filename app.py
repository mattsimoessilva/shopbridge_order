from flask import Flask, g
from flask_smorest import Api
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Blueprints
from controllers import order_blp as OrderController, address_blp as AddressController

# Repositories
from repositories.order_repository_impl import OrderRepository
from repositories.address_repository_impl import AddressRepository

# Services
from services.order_service_impl import OrderService
from services.address_service_impl import AddressService

# Mapper
from common.mapping.mapper_impl import Mapper

# SQLAlchemy Base
from models.entities.base import Base

DATABASE_URL = "sqlite+aiosqlite:///./order.db"


def create_app():
    app = Flask(__name__)

    # Swagger / OpenAPI config
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

    # Async DB engine and session factory
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session_factory = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Shared mapper
    mapper = Mapper()

    # Dependency injection
    order_repository = OrderRepository(session_factory=async_session_factory, mapper=mapper)
    order_service = OrderService(repository=order_repository, mapper=mapper)
    address_repository = AddressRepository(session_factory=async_session_factory, mapper=mapper)
    address_service = AddressService(repository=address_repository, mapper=mapper)

    # Store in app.extensions for controller access
    app.extensions.update(
        engine=engine,
        session_factory=async_session_factory,
        mapper=mapper,
        order_service=order_service,
        address_service=address_service
    )

    # Run startup logic immediately when app is created
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    import asyncio
    asyncio.run(startup())

    # Per-request session
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

    # Register blueprints
    api.register_blueprint(OrderController)
    api.register_blueprint(AddressController)

    return app


app = create_app()

if __name__ == "__main__":
    import asyncio
    try:
        from hypercorn.asyncio import serve
        from hypercorn.config import Config

        config = Config()
        config.bind = ["0.0.0.0:8000"]
        asyncio.run(serve(app, config))
    except ImportError:
        print("Hypercorn not installed. Falling back to Flask dev server.")
        app.run(debug=True)
