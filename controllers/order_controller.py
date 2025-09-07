from flask.views import MethodView
from flask_smorest import Blueprint, abort
from uuid import UUID
from models.schemas.order_request_schema import OrderRequestSchema
from models.schemas.order_response_schema import OrderResponseSchema
from services.interfaces.order_service_interface import OrderServiceInterface
from flask_smorest import Blueprint, abort


blp = Blueprint(
    "orders", "orders",
    url_prefix="/api/orders",
    description="Operations on orders"
)

class OrderController:
    order_service: OrderServiceInterface = None

    def list_orders(self):
        return  self.order_service.get_all_orders()

    def create_order(self, order_data):
        return  self.order_service.create_order(order_data)

    def get_order(self, order_id: UUID):
        order =  self.order_service.get_order_by_id(order_id)
        if not order:
            abort(404, message="Order not found")
        return order

    def update_order(self, order_data, order_id: UUID):
        order_data["id"] = order_id
        return  self.order_service.update_order_(order_data)

    def delete_order(self, order_id: UUID):
        success =  self.order_service.delete_order(order_id)
        if not success:
            abort(404, message="Order not found")

    # --- Registro das rotas ---
    @classmethod
    def register(cls, blp: Blueprint):
        controller = cls()

        blp.add_url_rule(
            "/", view_func=controller.list_orders, methods=["GET"]
        )
        blp.add_url_rule(
            "/", view_func=blp.arguments(OrderRequestSchema)(
                blp.response(201, OrderResponseSchema)(controller.create_order)
            ), methods=["POST"]
        )
        blp.add_url_rule(
            "/<uuid:order_id>", view_func=controller.get_order, methods=["GET"]
        )
        blp.add_url_rule(
            "/<uuid:order_id>", view_func=blp.arguments(OrderRequestSchema)(
                blp.response(200, OrderResponseSchema)(controller.update_order)
            ), methods=["PUT"]
        )
        blp.add_url_rule(
            "/<uuid:order_id>", view_func=blp.response(204)(controller.delete_order), methods=["DELETE"]
        )
