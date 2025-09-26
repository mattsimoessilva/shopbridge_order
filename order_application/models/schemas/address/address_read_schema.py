from datetime import datetime
from pydantic import BaseModel, Field, constr
from typing import Optional


class AddressReadSchema(BaseModel):
    id: str = Field(..., description="Unique identifier of the address")
    customer_id: str = Field(..., description="ID of the customer associated with the address")
    street: constr(max_length=100) = Field(..., description="Street address")
    city: constr(max_length=50) = Field(..., description="City")
    state: constr(max_length=50) = Field(..., description="State or province")
    postal_code: constr(max_length=20) = Field(..., description="Postal or ZIP code")
    country: constr(max_length=50) = Field(..., description="Country")
    created_at: datetime = Field(..., description="Timestamp when the address was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the address was last updated")
