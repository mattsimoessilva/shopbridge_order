from pydantic import BaseModel, Field
from typing import Optional


class OrderItemCreateSchema(BaseModel):
    product_id: str = Field(..., description="Product's unique identifier")
    product_variant_id: Optional[str] = Field(None, description="Product Variant's unique identifier")
    quantity: int = Field(..., description="Quantity of the product ordered")
    unit_price: Optional[float] = Field(None, description="Unit price of the product")

    @property
    def total_price(self) -> Optional[float]:
        if self.unit_price is not None and self.quantity is not None:
            return round(self.unit_price * self.quantity, 2)
        return None
