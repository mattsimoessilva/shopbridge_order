import uuid
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class OrderItemDTO:

    product_id: uuid.UUID

    quantity: int

    product_name: Optional[str] = field(default=None)

    unit_price: Optional[float] = field(default=None)

    @property
    def total_price(self) -> Optional[float]:
        if self.unit_price is None:
            return None
        return self.quantity * self.unit_price
