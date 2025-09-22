from marshmallow import Schema, fields
from models.schemas.order_item.order_item_read_schema import OrderItemReadSchema
from marshmallow.validate import OneOf
from models.enums import OrderStatus

class OrderUpdateSchema(Schema):
    id = fields.UUID(required=True)
    status = fields.String(
        required=True,
        validate=OneOf([status.value for status in OrderStatus]),
        metadata={"description": "Updated status of the order"}
    )