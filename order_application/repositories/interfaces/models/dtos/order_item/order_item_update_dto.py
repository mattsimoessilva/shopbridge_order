import uuid
from typing import Optional
from pydantic import BaseModel, condecimal


class OrderItemUpdateDTO(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[condecimal(max_digits=18, decimal_places=2)] = None

    class Config:
        from_attributes = True 
        use_enum_values = True
        json_encoders = {str: lambda v: str(v)}