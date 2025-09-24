from marshmallow import Schema, fields
from models.schemas.order_item.order_item_read_schema import OrderItemReadSchema
from marshmallow.validate import OneOf
from models.enums import OrderStatus

class OrderPatchSchema(Schema):
    status = fields.String(
        required=True,
        validate=OneOf([status.value for status in OrderStatus]),
        metadata={"description": "Patched status of the order"}
    )