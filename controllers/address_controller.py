# controllers/address_controller.py
from uuid import UUID
from flask import g, jsonify, current_app
from flask_smorest import Blueprint

from models.schemas.address.address_create_schema import AddressCreateSchema
from models.schemas.address.address_update_schema import AddressUpdateSchema
from models.schemas.address.address_read_schema import AddressReadSchema

blp = Blueprint(
    "addresses",
    "addresses",
    url_prefix="/api/addresses",
    description="Operations on Addresses"
)

@blp.route("/", methods=["POST"])
@blp.arguments(AddressCreateSchema)
@blp.response(201, AddressReadSchema)
async def Create(address_data):
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        result = await service.CreateAsync(address_data, session=session)
        return result
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@blp.route("/", methods=["GET"])
@blp.response(200, AddressReadSchema(many=True))
async def GetAll():
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        result = await service.GetAllAsync(session=session)
        return result
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@blp.route("/<uuid:address_id>", methods=["GET"])
@blp.response(200, AddressReadSchema)
async def GetById(address_id: UUID):
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        dto = await service.GetByIdAsync(address_id, session=session)
        if dto is None:
            return jsonify({"message": "Address not found"}), 404
        return dto
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@blp.route("/", methods=["PUT"])
@blp.arguments(AddressUpdateSchema)
@blp.response(200)
async def Update(address_data):
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        success = await service.UpdateAsync(address_data, session=session)
        if not success:
            return jsonify({"message": "Address not found"}), 404
        return {}, 200
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@blp.route("/<uuid:address_id>", methods=["DELETE"])
@blp.response(204)
async def Delete(address_id: UUID):
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        deleted = await service.DeleteAsync(address_id, session=session)
        if not deleted:
            return jsonify({"message": "Address not found"}), 404
        return "", 204
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
