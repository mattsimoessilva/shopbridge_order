from marshmallow import Schema, fields, validate


class AddressCreateSchema(Schema):
    customer_id = fields.String(required=True)
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

