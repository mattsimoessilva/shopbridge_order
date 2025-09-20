from marshmallow import Schema, fields
from models.schemas.order_item.order_item_read_schema import OrderItemReadSchema
from marshmallow.validate import OneOf
from models.enums import OrderStatus

class OrderUpdateSchema(Schema):
    id = fields.UUID(required=True)
    status = fields.String(
        required=False,
        validate=OneOf([status.value for status in OrderStatus]),
        metadata={"description": "Updated status of the order"}
    )
    deleted_at = fields.DateTime(required=False, allow_none=True, metadata={"description": "Timestamp for soft deletion"})