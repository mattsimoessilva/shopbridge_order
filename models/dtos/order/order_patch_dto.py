import uuid
from typing import List, Optional
from pydantic import BaseModel, condecimal
from models.enums import OrderStatus

class OrderPatchDTO(BaseModel):
    status: Optional[OrderStatus] = None
