from pydantic import BaseModel, Field
import uuid

class AddressCreateDTO(BaseModel):
    customer_id: str
    street: str = Field(..., max_length=100)
    city: str = Field(..., max_length=50)
    state: str = Field(..., max_length=50)
    postal_code: str = Field(..., max_length=20)
    country: str = Field(..., max_length=50)
