from pydantic import BaseModel, Field, constr
from typing import Optional


class AddressUpdateSchema(BaseModel):
    id: str = Field(..., description="Unique identifier of the address to update")
    street: Optional[constr(max_length=100)] = Field(None, description="Street address")
    city: Optional[constr(max_length=50)] = Field(None, description="City")
    state: Optional[constr(max_length=50)] = Field(None, description="State or province")
    postal_code: Optional[constr(max_length=20)] = Field(None, description="Postal or ZIP code")
    country: Optional[constr(max_length=50)] = Field(None, description="Country")
