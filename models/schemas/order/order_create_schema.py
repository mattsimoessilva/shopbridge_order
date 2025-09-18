from marshmallow import Schema, fields
from models.schemas.order_item_schema import OrderItemSchema

class OrderCreateSchema(Schema):
    customer_id = fields.UUID(required=True, metadata={"description": "Customer placing the order"})
    items = fields.List(fields.Nested(OrderItemSchema), required=True, metadata={"description": "List of items in the order"})