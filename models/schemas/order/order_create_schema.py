from marshmallow import Schema, fields
from models.schemas.order_item.order_item_read_schema import OrderItemReadSchema

class OrderCreateSchema(Schema):
    customer_id = fields.String(required=True, metadata={"description": "Customer placing the order"})
    items = fields.List(fields.Nested(OrderItemReadSchema), required=True, metadata={"description": "List of items in the order"})