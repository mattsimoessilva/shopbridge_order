from marshmallow import Schema, fields
from models.schemas.order_item_schema import OrderItemSchema 

class OrderRequestSchema(Schema):
    id = fields.UUID(dump_only=True, metadata={"description": "Order's unique identifier"})
    created_at = fields.DateTime(dump_only=True, metadata={"description": "Timestamp when the order was created"})
    updated_at = fields.DateTime(dump_only=True, metadata={"description": "Timestamp when the order was last updated"})
    
    customer_id = fields.UUID(required=True, metadata={"description": "Customer's unique identifier"})
    status = fields.String(dump_only=True, metadata={"description": "Current status of the order"})
    
    items = fields.List(
        fields.Nested(OrderItemSchema),
        required=True,
        metadata={"description": "List of items in the order"}
    )
