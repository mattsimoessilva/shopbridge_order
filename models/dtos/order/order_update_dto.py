import uuid
from typing import List, Optional
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus
from models.dtos.order_item.order_item_update_dto import OrderItemUpdateDTO


class OrderUpdateDTO(BaseModel):
    customer_id: Optional[uuid.UUID] = None
    total_amount: Optional[condecimal(max_digits=18, decimal_places=2)] = None
    status: Optional[OrderStatus] = None
    items: Optional[List[OrderItemUpdateDTO]] = None
