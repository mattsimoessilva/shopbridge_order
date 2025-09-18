# controllers/address_controller.py
from uuid import UUID
from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from marshmallow import ValidationError
from models.schemas.address.address_create_schema import AddressCreateSchema
from models.schemas.address.address_update_schema import AddressUpdateSchema
from models.dtos.address.address_create_dto import AddressCreateDTO
from models.dtos.address.address_update_dto import AddressUpdateDTO

blp = Blueprint(
    "addresses", "addresses",
    url_prefix="/api/addresses",
    description="Operations on Addresses"
)

@blp.route("/", methods=["POST"])
async def Create():
    """Creates a new Address."""
    try:
        data = request.get_json()
        validated_data = AddressCreateSchema().load(data)
        dto = AddressCreateDTO(**validated_data)

        service = current_app.extensions["address_service"]
        result = await service.CreateAsync(dto)

        return jsonify(result), HTTPStatus.CREATED

    except ValidationError as err:
        return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


@blp.route("/", methods=["GET"])
async def GetAll():
    """Retrieves all Addresses."""
    try:
        service = current_app.extensions["address_service"]
        result = await service.GetAllAsync()
        return jsonify(result), HTTPStatus.OK
    except Exception as ex:
        return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


@blp.route("/<uuid:address_id>", methods=["GET"])
async def GetById(address_id: UUID):
    """Retrieves a specific Address by ID."""
    try:
        service = current_app.extensions["address_service"]
        result = await service.GetByIdAsync(address_id)
        if not result:
            return jsonify({"message": "Address not found"}), HTTPStatus.NOT_FOUND
        return jsonify(result), HTTPStatus.OK
    except Exception as ex:
        return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


@blp.route("/", methods=["PUT"])
async def Update():
    """Updates an Address record."""
    try:
        data = request.get_json()
        validated_data = AddressUpdateSchema().load(data)
        dto = AddressUpdateDTO(**validated_data)

        service = current_app.extensions["address_service"]
        success = await service.UpdateAsync(dto)

        if not success:
            return jsonify({"message": "Address not found"}), HTTPStatus.NOT_FOUND
        return "", HTTPStatus.OK

    except ValidationError as err:
        return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


@blp.route("/<uuid:address_id>", methods=["DELETE"])
async def Delete(address_id: UUID):
    """Deletes an Address by ID."""
    try:
        service = current_app.extensions["address_service"]
        deleted = await service.DeleteAsync(address_id)
        if not deleted:
            return jsonify({"message": "Address not found"}), HTTPStatus.NOT_FOUND
        return "", HTTPStatus.NO_CONTENT
    except Exception as ex:
        return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR
