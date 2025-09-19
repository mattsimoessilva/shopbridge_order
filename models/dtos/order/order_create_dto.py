import uuid
from typing import List
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus
from models.dtos.order_item.order_item_create_dto import OrderItemCreateDTO


class OrderCreateDTO(BaseModel):
    customer_id: uuid.UUID
    total_amount: condecimal(max_digits=18, decimal_places=2)
    status: OrderStatus
    items: List[OrderItemCreateDTO]
