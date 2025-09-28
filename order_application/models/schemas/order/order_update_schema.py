from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from models.enums import OrderStatus
from models.schemas.order_item import OrderItemUpdateSchema

class OrderUpdateSchema(BaseModel):
    items: List[OrderItemUpdateSchema] = Field(..., description="List of order items to update (quantities only)")

    class Config:
        from_attributes = True
