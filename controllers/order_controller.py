from flask import request, jsonify, url_for, Response
from flask_classful import FlaskView, route

from models.dtos.order_request_dto import OrderRequestDTO
from models.dtos.order_response_dto import OrderResponseDTO
from services.order_service_interface import OrderServiceInterface


class OrdersController(FlaskView):
    route_base = "/api/orders/"

    def __init__(self, order_service: OrderServiceInterface):
        self._order_service = order_service

    # POST: Create order
    @route("", methods=["POST"])
    async def create(self):
        data = request.get_json()
        order_request = OrderRequestDTO(**data)

        created_order = await self._order_service.create_order_async(order_request)
        location = url_for('OrdersController:get_by_id', order_id=created_order.id)

        return jsonify(created_order.__dict__), 201, {"Location": location}

    # GET: All orders
    @route("", methods=["GET"])
    async def get_all(self):
        orders = await self._order_service.get_all_orders_async()
        return jsonify([o.__dict__ for o in orders]), 200

    # GET: Order by ID
    @route("<string:order_id>", methods=["GET"])
    async def get_by_id(self, order_id: str):
        order = await self._order_service.get_order_by_id_async(order_id)
        if order is None:
            return Response(status=404)
        return jsonify(order.__dict__), 200

    # PUT: Update order
    @route("", methods=["PUT"])
    async def update(self):
        data = request.get_json()
        order_request = OrderRequestDTO(**data)
        updated_order = await self._order_service.update_order_async(order_request)
        return jsonify(updated_order.__dict__), 200

    # DELETE: Remove order
    @route("<string:order_id>", methods=["DELETE"])
    async def delete(self, order_id: str):
        success = await self._order_service.delete_order_async(order_id)
        if not success:
            return Response(status=404)
        return Response(status=204)
