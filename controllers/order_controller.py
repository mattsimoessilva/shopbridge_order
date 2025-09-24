from uuid import UUID
from flask import g, jsonify, current_app
from flask_smorest import Blueprint

from models.schemas.order.order_create_schema import OrderCreateSchema
from models.schemas.order.order_update_schema import OrderUpdateSchema
from models.schemas.order.order_read_schema import OrderReadSchema
from models.schemas.order.order_patch_schema import OrderPatchSchema


blp = Blueprint(
    "orders",
    "orders",
    url_prefix="/api/orders",
    description="Operations on Orders"
)


@blp.route("/", methods=["POST"])
@blp.arguments(OrderCreateSchema)
@blp.response(201, OrderReadSchema)
async def Create(data):
    """Creates a new Order."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        result = await service.CreateAsync(data, session=session)
        return result

    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/", methods=["GET"])
@blp.response(200, OrderReadSchema(many=True))
async def GetAll():
    """Retrieves all Orders."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        result = await service.GetAllAsync(session=session)
        return result

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/<uuid:id>", methods=["GET"])
@blp.response(200, OrderReadSchema)
async def GetById(id: UUID):
    """Retrieves a specific Order by ID."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        dto = await service.GetByIdAsync(id, session=session)
        if dto is None:
            return jsonify({"message": "Record not found"}), 404

        return dto

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/<uuid:id>", methods=["PUT"])
@blp.arguments(OrderUpdateSchema)
@blp.response(200)
async def Update(data, id):
    """Updates an Order record."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        success = await service.UpdateAsync(data, session=session)
        if not success:
            return jsonify({"message": "Record not found"}), 404

        return {}, 200

    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@blp.route("/<uuid:id>", methods=["DELETE"])
@blp.response(204)
async def Delete(id: UUID):
    """Deletes an Order by ID."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        deleted = await service.DeleteAsync(id, session=session)
        if not deleted:
            return jsonify({"message": "Record not found"}), 404

        return "", 204

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@blp.route("/<uuid:id>", methods=["PATCH"])
@blp.arguments(OrderPatchSchema(partial=True))
@blp.response(200, OrderReadSchema)
async def Patch(data, id: UUID):
    """Partially updates an Order (e.g., status transitions)."""
    try:
        session = g.db
        service = current_app.extensions["order_service"]

        updated = await service.PatchAsync(id, data, session=session)
        if not updated:
            return jsonify({"message": "Record not found"}), 404

        dto = await service.GetByIdAsync(id, session=session)
        return dto

    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
