from marshmallow import Schema, fields, validate

class AddressUpdateSchema(Schema):
    id = fields.UUID(required=True)
    street = fields.String(
        required=False,
        validate=validate.Length(max=100)
    )
    city = fields.String(
        required=False,
        validate=validate.Length(max=50)
    )
    state = fields.String(
        required=False,
        validate=validate.Length(max=50)
    )
    postal_code = fields.String(
        required=False,
        validate=validate.Length(max=20)
    )
    country = fields.String(
        required=False,
        validate=validate.Length(max=50)
    )
