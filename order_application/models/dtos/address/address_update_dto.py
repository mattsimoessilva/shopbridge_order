from typing import Optional
from pydantic import BaseModel, Field
import uuid

class AddressUpdateDTO(BaseModel):
    id: str
    street: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    state: Optional[str] = Field(None, max_length=50)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True 
        use_enum_values = True
        json_encoders = {str: lambda v: str(v)}