import uuid
from typing import List, Optional
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus
from models.dtos.order_item.order_item_update_dto import OrderItemUpdateDTO


class OrderUpdateDTO(BaseModel):
    id: uuid.UUID
    status: Optional[OrderStatus] = None
