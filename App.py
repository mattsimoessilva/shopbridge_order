from flask import Flask
from flask_smorest import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.order_controller import blp, OrderController
from repositories.order_repository_impl import OrderRepository
from services.order_service_impl import OrderService
from models.entities.base import Base

DATABASE_URL = "sqlite:///./order.db"

def create_app():
    app = Flask(__name__)

    # Create database
    engine = create_engine("sqlite:///./order.db", echo=True, future=True)
    Base.metadata.create_all(engine)


    # Swagger / OpenAPI config
    app.config["API_TITLE"] = "Order API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Initialize Swagger API
    api = Api(app)

    # Create DB engine and session
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    SessionLocal = sessionmaker(bind=engine)

    # Dependency injection
    repo = OrderRepository(sync_session=SessionLocal())
    service = OrderService(repository=repo)

    OrderController.order_service = service
    OrderController.register(blp)
    api.register_blueprint(blp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)