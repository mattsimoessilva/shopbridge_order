from flask import Flask
from flask_smorest import Api
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from controllers.order_controller import blp, OrderController
from repositories.order_repository_impl import OrderRepository
from services.order_service_impl import OrderService
from models.entities.base import Base

DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./order.db"
DATABASE_URL_SYNC = "sqlite:///./order.db"

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

    # Create DB engines
    async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True, future=True)
    sync_engine = create_engine(DATABASE_URL_SYNC, echo=True, future=True)

    # Create sessions
    AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
    SyncSessionLocal = sessionmaker(bind=sync_engine)


    # Dependency injection
    repo = OrderRepository(async_session=AsyncSessionLocal(), sync_session=SyncSessionLocal())
    service = OrderService(repository=repo)

    OrderController.order_service = service
    OrderController.register(blp)
    api.register_blueprint(blp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
