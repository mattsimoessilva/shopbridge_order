from flask.views import MethodView
from flask_smorest import Blueprint
from uuid import UUID
from models.schemas.order_request_schema import OrderRequestSchema
from models.schemas.order_response_schema import OrderResponseSchema
from services.interfaces.order_service_interface import OrderServiceInterface
from flask_smorest import Blueprint

blp = Blueprint(
    "orders", "orders",
    url_prefix="/api/orders",
    description="Operations on orders"
)

class OrderController:
    order_service: OrderServiceInterface = None

    async def list_orders(self):
        return await self.order_service.get_all_orders_async()

    async def create_order(self, order_data):
        return await self.order_service.create_order_async(order_data)

    async def get_order(self, order_id: UUID):
        order = await self.order_service.get_order_by_id_async(order_id)
        if not order:
            blp.abort(404, message="Order not found")
        return order

    async def update_order(self, order_data, order_id: UUID):
        order_data["id"] = order_id
        return await self.order_service.update_order_async(order_data)

    async def delete_order(self, order_id: UUID):
        success = await self.order_service.delete_order_async(order_id)
        if not success:
            blp.abort(404, message="Order not found")

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
