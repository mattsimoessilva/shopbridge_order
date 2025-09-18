# app.py
from flask import Flask, g
from flask_smorest import Api
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from controllers.order_controller import blp as order_blp, OrderController
from repositories.order_repository_impl import OrderRepository
from services.order_service_impl import OrderService
from services.mapping.mapper_impl import Mapper
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

    # Async DB engine and session factory (global, not per request)
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session_factory = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Store factories and singletons in app.extensions (DI container)
    mapper = Mapper()
    repository = OrderRepository(session_factory=async_session_factory, mapper=mapper)
    service = OrderService(repository=repository, mapper=mapper)

    app.extensions["engine"] = engine
    app.extensions["session_factory"] = async_session_factory
    app.extensions["mapper"] = mapper
    app.extensions["order_service"] = service

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
        # Create but don’t start a transaction; let repository manage as needed
        g.db = async_session_factory()

    @app.teardown_request
    async def close_session(exc):
        session = getattr(g, "db", None)
        if session is not None:
            await session.close()

    # Inject service into controller and register blueprint
    order_controller = OrderController(service=service)
    api.register_blueprint(order_blp)

    return app

app = create_app()

if __name__ == "__main__":
    # Dev only. Async support is limited in the built-in server.
    # For proper async, run with an ASGI server (see run instructions below).
    app.run(debug=True)
