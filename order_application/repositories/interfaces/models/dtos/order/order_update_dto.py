import uuid
from typing import List, Optional
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus
from models.dtos.order_item import OrderItemUpdateDTO
from decimal import Decimal


class OrderUpdateDTO(BaseModel):
    customer_id: str
    shipment_id: Optional[str] = None
    total_amount: Decimal
    status: OrderStatus
    items: List[OrderItemUpdateDTO]

    class Config:
        from_attributes = True 
        use_enum_values = True
        json_encoders = {str: lambda v: str(v)}