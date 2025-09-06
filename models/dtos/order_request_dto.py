import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from models.dtos.order_item_dto import OrderItemDTO
from models.entities.order_status import OrderStatus


@dataclass
class OrderRequestDTO:

    id: Optional[uuid.UUID] = None

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    customer_id: uuid.UUID = field(default_factory=uuid.uuid4)

    status: Optional[OrderStatus] = None

    items: List[OrderItemDTO] = field(default_factory=list)
