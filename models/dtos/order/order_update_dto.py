import uuid
from typing import List, Optional
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus
from models.dtos.order_item.order_item_update_dto import OrderItemUpdateDTO


class OrderUpdateDTO(BaseModel):
    customer_id: str
    shipment_id: Optional[OrderStatus] = None
    total_amount: float
    status: OrderStatus
    items: List["OrderItemUpdateDTO"]


