import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AddressReadDTO(BaseModel):
    id: uuid.UUID
    customer_id: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
