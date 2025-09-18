from flask import Flask
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

    # Initialize Swagger API
    api = Api(app)

    # Create async DB engine and session factory
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session_factory = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Create tables (sync call via run_sync)
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    import asyncio
    asyncio.run(init_models())

    # Dependency injection
    mapper = Mapper()
    repo = OrderRepository(session=async_session_factory(), mapper=mapper)
    service = OrderService(repository=repo, mapper=mapper)

    # Inject service into controller
    order_controller = OrderController(service)
    api.register_blueprint(order_blp)

    return app


app = create_app()

if __name__ == "__main__":
    # For async routes, better to run with hypercorn or uvicorn:
    # hypercorn app:app --reload
    app.run(debug=True)
