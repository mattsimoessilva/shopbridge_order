from uuid import UUID
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from services.interfaces.address_service_interface import AddressServiceInterface
from models.schemas.address.address_create_schema import AddressCreateSchema
from models.schemas.address.address_update_schema import AddressUpdateSchema
from models.dtos.address.address_create_dto import AddressCreateDTO
from models.dtos.address.address_update_dto import AddressUpdateDTO
from marshmallow import ValidationError


blp = Blueprint("addresses", __name__, url_prefix="/api/addresses")


class AddressController:

    def __init__(self, service: AddressServiceInterface):
        self._service = service


    @blp.route("/", methods=["POST"])
    async def create(self):
        """Creates a new Address."""
        try:
            data = request.get_json()

            validated_data = AddressCreateSchema().load(data)

            dto = AddressCreateDTO(**validated_data)

            result = await self._service.create_async(dto)

            return jsonify(result), HTTPStatus.CREATED

        except ValidationError as err:
            return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST

        except Exception as ex:
            return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


    @blp.route("/", methods=["GET"])
    async def get_all(self):
        """Retrieves all Addresses."""
        try:
            result = await self._service.get_all_async()

            return jsonify(result), HTTPStatus.OK

        except Exception as ex:
            return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


    @blp.route("/<uuid:address_id>", methods=["GET"])
    async def get_by_id(self, address_id: UUID):
        """Retrieves a specific Address by ID."""
        try:
            result = await self._service.get_by_id_async(address_id)

            if not result:
                return jsonify({"message": "Address not found"}), HTTPStatus.NOT_FOUND

            return jsonify(result), HTTPStatus.OK

        except Exception as ex:
            return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


    @blp.route("/", methods=["PUT"])
    async def update(self):
        """Updates an Address record."""
        try:
            data = request.get_json()

            validated_data = AddressUpdateSchema().load(data)

            dto = AddressUpdateDTO(**validated_data)

            success = await self._service.update_async(dto)

            if not success:
                return jsonify({"message": "Address not found"}), HTTPStatus.NOT_FOUND

            return "", HTTPStatus.OK

        except ValidationError as err:
            return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST

        except Exception as ex:
            return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR


    @blp.route("/<uuid:address_id>", methods=["DELETE"])
    async def delete(self, address_id: UUID):
        """Deletes an Address by ID."""
        try:
            deleted = await self._service.delete_async(address_id)

            if not deleted:
                return jsonify({"message": "Address not found"}), HTTPStatus.NOT_FOUND

            return "", HTTPStatus.NO_CONTENT

        except Exception as ex:
            return jsonify({"error": str(ex)}), HTTPStatus.INTERNAL_SERVER_ERROR
