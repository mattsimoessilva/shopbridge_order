import uuid
from typing import Optional
from sqlalchemy import ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.entities.base import Base
from models.entities.order import Order

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True)
  

    order_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("orders.id"), nullable=False
    )

    product_id: Mapped[str] = mapped_column(String(36), nullable=False)

    product_variant_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    unit_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="items")

    @property
    def total_price(self) -> Optional[float]:
        if self.unit_price is not None and self.quantity is not None:
            return round(self.unit_price * self.quantity, 2)
        return None

    def __repr__(self) -> str:
        return (
            f"<OrderItem product_id={self.product_id} "
            f"quantity={self.quantity} unit_price={self.unit_price}>"
        )
