import uuid
from pydantic import BaseModel


class OrderItemReadDTO(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        orm_mode = True
