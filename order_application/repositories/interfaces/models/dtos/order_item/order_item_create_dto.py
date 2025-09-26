import uuid
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, condecimal


class OrderItemCreateDTO(BaseModel):
    product_id: str
    product_variant_id: Optional[str] = None
    quantity: int
    unit_price: Optional[condecimal(max_digits=18, decimal_places=2)] = None

    class Config:
        from_attributes = True 
        use_enum_values = True
        json_encoders = {str: lambda v: str(v)}