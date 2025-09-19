import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from models.enums import OrderStatus
from models.dtos.order_item.order_item_read_dto import OrderItemReadDTO


class OrderReadDTO(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    customer_id: uuid.UUID
    total_amount: float
    status: OrderStatus
    items: List[OrderItemReadDTO] = []

    class Config:
        orm_mode = True
