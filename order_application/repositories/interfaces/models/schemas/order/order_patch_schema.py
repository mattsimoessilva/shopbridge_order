from pydantic import BaseModel, Field
from typing import Optional
from models.enums import OrderStatus

class OrderPatchSchema(BaseModel):
    status: OrderStatus = Field(..., description="Patched status of the order")
