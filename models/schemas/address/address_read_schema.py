from marshmallow import Schema, fields, validate

class AddressReadSchema(Schema):
    id = fields.UUID(required=True)
    street = fields.String(
        required=True,
        validate=validate.Length(max=100)
    )
    city = fields.String(
        required=True,
        validate=validate.Length(max=50)
    )
    state = fields.String(
        required=True,
        validate=validate.Length(max=50)
    )
    postal_code = fields.String(
        required=True,
        validate=validate.Length(max=20)
    )
    country = fields.String(
        required=True,
        validate=validate.Length(max=50)
    )
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(allow_none=True)
    deleted_at = fields.DateTime(allow_none=True)
