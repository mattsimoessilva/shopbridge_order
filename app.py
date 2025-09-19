from flask import Flask, g
from flask_smorest import Api
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Blueprint aliases from controllers/__init__.py
from controllers import order_blp as OrderController, address_blp as AddressController

# Repositories
from repositories.order_repository_impl import OrderRepository
from repositories.address_repository_impl import AddressRepository

# Services
from services.order_service_impl import OrderService
from services.address_service_impl import AddressService

# Shared mapper
from services.mapping.mapper_impl import Mapper

# SQLAlchemy Base
from models.entities.base import Base

DATABASE_URL = "sqlite+aiosqlite:///./order.db"


def create_app():
    app = Flask(__name__)

    # Swagger / OpenAPI config
    app.config["API_TITLE"] = "Order API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_JSON_PATH"] = "openapi.json"

    # Initialize Swagger API
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

    # Dependency injection: repositories & services
    order_repository = OrderRepository(session_factory=async_session_factory, mapper=mapper)
    order_service = OrderService(repository=order_repository, mapper=mapper)

    address_repository = AddressRepository(session_factory=async_session_factory, mapper=mapper)
    address_service = AddressService(repository=address_repository, mapper=mapper)

    # Store in app.extensions for controller access
    app.extensions["engine"] = engine
    app.extensions["session_factory"] = async_session_factory
    app.extensions["mapper"] = mapper
    app.extensions["order_service"] = order_service
    app.extensions["address_service"] = address_service

    # Async startup/shutdown hooks
    @app.before_serving
    async def startup():
        # Create tables once at startup (dev). Prefer Alembic migrations in prod.
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.after_serving
    async def shutdown():
        await engine.dispose()

    # Per-request session: create on request start, close on teardown
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
                pass  # Avoid masking original exceptions

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
