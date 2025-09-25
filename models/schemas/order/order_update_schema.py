from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from models.enums import OrderStatus
from models.schemas.order_item.order_item_read_schema import OrderItemReadSchema

class OrderUpdateSchema(BaseModel):
    customer_id: str = Field(..., description="Identifier of the customer placing the order")
    shipment_id: Optional[str] = Field(None, description="Identifier of the shipment associated with the order")
    total_amount: Decimal = Field(..., description="Total amount of the order")
    status: OrderStatus = Field(..., description="Updated status of the order")
    items: List[OrderItemReadSchema] = Field(..., description="List of items in the order (full replacement)")
