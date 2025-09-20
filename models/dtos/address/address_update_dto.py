from typing import Optional
from pydantic import BaseModel, Field
import uuid

class AddressUpdateDTO(BaseModel):
    id: uuid.UUID
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    state: Optional[str] = Field(None, max_length=50)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=50)
