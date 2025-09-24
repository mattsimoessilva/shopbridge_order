from marshmallow import Schema, fields
from models.schemas.order_item.order_item_read_schema import OrderItemReadSchema
from marshmallow.validate import OneOf
from models.enums import OrderStatus

class OrderUpdateSchema(Schema):
    customer_id = fields.String(
        required=True,
        metadata={"description": "Identifier of the customer placing the order"}
    )
    shipment_id = fields.String(
        required=False,
        allow_none=True,
        metadata={"description": "Identifier of the shipment associated with the order"}
    )
    total_amount = fields.Decimal(
        required=True,
        as_string=True,
        metadata={"description": "Total amount of the order"}
    )
    status = fields.String(
        required=True,
        validate=OneOf([status.value for status in OrderStatus]),
        metadata={"description": "Updated status of the order"}
    )
    items = fields.List(
        fields.Nested(OrderItemReadSchema),
        required=True,
        metadata={"description": "List of items in the order (full replacement)"}
    )
