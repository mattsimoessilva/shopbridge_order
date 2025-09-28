from pydantic import BaseModel, Field

class OrderItemUpdateSchema(BaseModel):
    id: str = Field(..., description="Unique identifier of the order item")
    quantity: int = Field(..., gt=0, description="Updated quantity of the product in the order")

    class Config:
        from_attributes = True
