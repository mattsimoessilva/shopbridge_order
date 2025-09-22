from typing import Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel

class OrderItemReadDTO(BaseModel):
    id: Optional[UUID] = None
    product_id: UUID
    product_variant_id: Optional[UUID] = None
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        orm_mode = True
