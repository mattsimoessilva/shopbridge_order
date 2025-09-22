import uuid
from typing import List
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus
from models.dtos.order_item.order_item_create_dto import OrderItemCreateDTO


class OrderCreateDTO(BaseModel):
    customer_id: str
    items: List[OrderItemCreateDTO]
