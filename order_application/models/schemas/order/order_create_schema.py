from typing import List
from pydantic import BaseModel, Field
from models.schemas.order_item import OrderItemCreateSchema

class OrderCreateSchema(BaseModel):
    customer_id: str = Field(..., description="Customer placing the order")
    items: List[OrderItemCreateSchema] = Field(..., description="List of items in the order")
