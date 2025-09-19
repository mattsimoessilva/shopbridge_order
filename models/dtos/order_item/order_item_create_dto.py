import uuid
from pydantic import BaseModel, condecimal


class OrderItemCreateDTO(BaseModel):
    product_id: uuid.UUID
    quantity: int
    unit_price: condecimal(max_digits=18, decimal_places=2)
