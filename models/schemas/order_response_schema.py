from marshmallow import Schema, fields
from models.schemas.order_item_schema import OrderItemSchema

class OrderResponseSchema(Schema):
    id = fields.UUID(required=True, metadata={"description": "Order's unique identifier"})
    created_at = fields.DateTime(required=True, metadata={"description": "Timestamp when the order was created"})
    customer_id = fields.UUID(required=True, metadata={"description": "Customer's unique identifier"})
    status = fields.String(required=True, metadata={"description": "Current status of the order"})

    items = fields.List(
        fields.Nested(OrderItemSchema),
        required=True,
        metadata={"description": "List of items in the order"}
    )

    total_amount = fields.Float(required=True, metadata={"description": "Total amount for the order"})
