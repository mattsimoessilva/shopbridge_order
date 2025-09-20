from uuid import UUID
from flask import request, jsonify, current_app, g
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError

from models.schemas.address.address_create_schema import AddressCreateSchema
from models.schemas.address.address_update_schema import AddressUpdateSchema
from models.dtos.address.address_create_dto import AddressCreateDTO
from models.dtos.address.address_update_dto import AddressUpdateDTO

blp = Blueprint(
    "addresses",
    "addresses",
    url_prefix="/api/addresses",
    description="Operations on Addresses"
)

@blp.route("/", methods=["POST"])
@blp.arguments(AddressCreateSchema)
@blp.response(HTTPStatus.CREATED)
async def Create(address_data):
    """Creates a new Address."""
    try:
        dto = AddressCreateDTO(**address_data)
        session = g.db
        service = current_app.extensions["address_service"]
        return await service.CreateAsync(dto, session=session)
    except ValidationError as err:
        return {"errors": err.messages}, HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return {"error": str(ex)}, HTTPStatus.INTERNAL_SERVER_ERROR

@blp.route("/", methods=["GET"])
@blp.response(HTTPStatus.OK)
async def GetAll():
    """Retrieves all Addresses."""
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        return await service.GetAllAsync(session=session)
    except Exception as ex:
        return {"error": str(ex)}, HTTPStatus.INTERNAL_SERVER_ERROR

@blp.route("/<uuid:address_id>", methods=["GET"])
@blp.response(HTTPStatus.OK)
async def GetById(address_id: UUID):
    """Retrieves a specific Address by ID."""
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        result = await service.GetByIdAsync(address_id, session=session)
        if not result:
            return {"message": "Address not found"}, HTTPStatus.NOT_FOUND
        return result
    except Exception as ex:
        return {"error": str(ex)}, HTTPStatus.INTERNAL_SERVER_ERROR

@blp.route("/", methods=["PUT"])
@blp.arguments(AddressUpdateSchema)
@blp.response(HTTPStatus.OK)
async def Update(address_data):
    """Updates an Address record."""
    try:
        dto = AddressUpdateDTO(**address_data)
        session = g.db
        service = current_app.extensions["address_service"]
        success = await service.UpdateAsync(dto, session=session)
        if not success:
            return {"message": "Address not found"}, HTTPStatus.NOT_FOUND
        return {}
    except ValidationError as err:
        return {"errors": err.messages}, HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return {"error": str(ex)}, HTTPStatus.INTERNAL_SERVER_ERROR

@blp.route("/<uuid:address_id>", methods=["DELETE"])
@blp.response(HTTPStatus.NO_CONTENT)
async def Delete(address_id: UUID):
    """Deletes an Address by ID."""
    try:
        session = g.db
        service = current_app.extensions["address_service"]
        deleted = await service.DeleteAsync(address_id, session=session)
        if not deleted:
            return {"message": "Address not found"}, HTTPStatus.NOT_FOUND
        return ""
    except Exception as ex:
        return {"error": str(ex)}, HTTPStatus.INTERNAL_SERVER_ERROR
