import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from models.dtos.order_item_dto import OrderItemDTO
from models.entities.order_status import OrderStatus


@dataclass
class OrderResponseDTO:
    id: uuid.UUID

    created_at: datetime

    customer_id: uuid.UUID

    status: OrderStatus

    items: List[OrderItemDTO] = field(default_factory=list)

    total_amount: float = 0.0
