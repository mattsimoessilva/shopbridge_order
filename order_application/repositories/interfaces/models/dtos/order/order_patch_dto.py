import uuid
from typing import Optional
from pydantic import BaseModel
from models.enums import OrderStatus

class OrderPatchDTO(BaseModel):
    status: Optional[OrderStatus] = None

    class Config:
        use_enum_values = True  # Ensures enum values are serialized as strings
        orm_mode = True         # Allows compatibility with SQLAlchemy ORM objects
