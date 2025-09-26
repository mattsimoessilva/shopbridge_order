import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from models.enums import OrderStatus
from models.dtos.order_item import OrderItemReadDTO
from decimal import Decimal


class OrderReadDTO(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    customer_id: str
    shipment_id: Optional[str] = None
    total_amount: Decimal
    status: OrderStatus
    items: List[OrderItemReadDTO] = []

    class Config:
        from_attributes = True 
        use_enum_values = True
        json_encoders = {str: lambda v: str(v)}