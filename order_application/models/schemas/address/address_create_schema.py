from pydantic import BaseModel, Field, constr

class AddressCreateSchema(BaseModel):
    customer_id: str = Field(..., description="ID of the customer associated with the address")
    street: constr(max_length=100) = Field(..., description="Street address")
    city: constr(max_length=50) = Field(..., description="City")
    state: constr(max_length=50) = Field(..., description="State or province")
    postal_code: constr(max_length=20) = Field(..., description="Postal or ZIP code")
    country: constr(max_length=50) = Field(..., description="Country")
