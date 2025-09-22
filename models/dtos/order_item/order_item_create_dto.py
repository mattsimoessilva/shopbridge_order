import uuid
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, condecimal

class OrderItemCreateDTO(BaseModel):
    product_id: uuid.UUID
    quantity: int
    unit_price: Optional[condecimal(max_digits=18, decimal_places=2)] = None
