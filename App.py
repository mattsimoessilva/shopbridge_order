from flask import Flask
from flask_classful import FlaskView
from controllers.orders_controller import OrdersController
from services.order_service_impl import OrderService  # your concrete implementation

app = Flask(__name__)

# Dependency injection
order_service = OrderService()

# Register the controller
OrdersController.register(app, init_argument=order_service)

if __name__ == "__main__":
    app.run(debug=True)
