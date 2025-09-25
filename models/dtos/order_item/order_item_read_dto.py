from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
import uuid

class OrderItemReadDTO(BaseModel):
    id: Optional[str] = None
    product_id: str
    product_variant_id: Optional[str] = None
    quantity: int
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None

    class Config:
        from_attributes = True 
        use_enum_values = True
        json_encoders = {str: lambda v: str(v)}