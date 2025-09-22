from datetime import datetime
from marshmallow import Schema, fields, validate
from models.enums import OrderStatus
from models.schemas.order_item import OrderItemReadSchema

class OrderReadSchema(Schema):
    id = fields.UUID(required=True, dump_only=True)
    created_at = fields.DateTime(required=True, dump_only=True)
    updated_at = fields.DateTime(allow_none=True, dump_only=True)
    deleted_at = fields.DateTime(allow_none=True, dump_only=True)
    customer_id = fields.String(required=True) 
    shipment_id = fields.String(allow_none=True)  
    total_amount = fields.Decimal(as_string=True, required=True)
    status = fields.String(
        required=True,
        validate=validate.OneOf([status.value for status in OrderStatus])
    )
    items = fields.List(fields.Nested(OrderItemReadSchema), dump_only=True)
