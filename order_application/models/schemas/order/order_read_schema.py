from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from models.enums import OrderStatus
from models.schemas.order_item import OrderItemReadSchema
import uuid

class OrderReadSchema(BaseModel):
    id: str = Field(..., description="Unique identifier of the order")
    created_at: datetime = Field(..., description="Timestamp when the order was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the order was last updated")
    customer_id: str = Field(..., description="ID of the customer who placed the order")
    shipment_id: Optional[str] = Field(None, description="ID of the associated shipment, if any")
    total_amount: Decimal = Field(..., description="Total amount of the order")
    status: OrderStatus = Field(..., description="Current status of the order")
    items: List[OrderItemReadSchema] = Field(..., description="List of items in the order")

    class Config:
        json_encoders = {str: lambda v: str(v)}
