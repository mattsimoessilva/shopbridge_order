import uuid
from typing import Optional
from pydantic import BaseModel, condecimal, Field

class OrderItemUpdateDTO(BaseModel):
    id: str = Field(..., description="Unique identifier of the order item")
    quantity: int = Field(..., description="Updated quantity of the item")

    class Config:
        from_attributes = True
