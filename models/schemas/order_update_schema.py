from marshmallow import Schema, fields
from models.schemas.order_item_schema import OrderItemSchema
from marshmallow.validate import OneOf
from models.enums import OrderStatus

class OrderUpdateSchema(Schema):
    status = fields.String(
        required=False,
        validate=OneOf([status.value for status in OrderStatus]),
        metadata={"description": "Updated status of the order"}
    )
    items = fields.List(fields.Nested(OrderItemSchema), required=False, metadata={"description": "Updated list of items"})
    deleted_at = fields.DateTime(required=False, allow_none=True, metadata={"description": "Timestamp for soft deletion"})