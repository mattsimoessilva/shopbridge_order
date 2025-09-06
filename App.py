from flask import Flask
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from controllers.orders_controller import OrdersController
from repositories.order_repository_impl import OrderRepository
from services.order_service_impl import OrderService
from models.entities.base import Base

# SQLite connection strings
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./order.db"
DATABASE_URL_SYNC = "sqlite:///./order.db"

def create_app():
    app = Flask(__name__)

    # Create DB engines
    async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True, future=True)
    sync_engine = create_engine(DATABASE_URL_SYNC, echo=True, future=True)

    # Create sessions
    AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
    SyncSessionLocal = sessionmaker(bind=sync_engine)

    # Create tables (sync for simplicity here)
    Base.metadata.create_all(bind=sync_engine)

    # Dependency injection
    repo = OrderRepository(async_session=AsyncSessionLocal(), sync_session=SyncSessionLocal())
    service = OrderService(repository=repo)

    # Register controller
    OrdersController.register(app, init_argument=service)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
