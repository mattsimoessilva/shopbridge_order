# controllers/order_controller.py

from uuid import UUID
from flask import g, jsonify, current_app
from flask_smorest import Blueprint

from models.schemas.order_create_schema import OrderCreateSchema
from models.schemas.order_update_schema import OrderUpdateSchema
from models.schemas.order_schema import OrderSchema


blp = Blueprint(
    "orders",
    "orders",
    url_prefix="/api/orders",
    description="Operations on Orders"
)


@blp.route("/", methods=["POST"])
@blp.arguments(OrderCreateSchema)
@blp.response(201, OrderSchema)
async def Create(order_data):
    """Creates a new Order."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        result = await service.CreateAsync(order_data, session=session)
        return result

    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/", methods=["GET"])
@blp.response(200, OrderSchema(many=True))
async def GetAll():
    """Retrieves all Orders."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        result = await service.GetAllAsync(session=session)
        return result

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/<uuid:order_id>", methods=["GET"])
@blp.response(200, OrderSchema)
async def GetById(order_id: UUID):
    """Retrieves a specific Order by ID."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        dto = await service.GetByIdAsync(order_id, session=session)
        if dto is None:
            return jsonify({"message": "Order not found"}), 404

        return dto

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/", methods=["PUT"])
@blp.arguments(OrderUpdateSchema)
@blp.response(200)
async def Update(order_data):
    """Updates an Order record."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        success = await service.UpdateAsync(order_data, session=session)
        if not success:
            return jsonify({"message": "Order not found"}), 404

        return {}, 200

    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/<uuid:order_id>", methods=["DELETE"])
@blp.response(204)
async def Delete(order_id: UUID):
    """Deletes an Order by ID."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        deleted = await service.DeleteAsync(order_id, session=session)
        if not deleted:
            return jsonify({"message": "Order not found"}), 404

        return "", 204

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
