import uuid
from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.entities.base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )

    product_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)

    product_variant_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    unit_price: Mapped[float] = mapped_column(Float, nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="items")

    @property
    def total_price(self) -> float | None:
        if self.unit_price is not None and self.quantity is not None:
            return round(self.unit_price * self.quantity, 2)
        return None

    def __repr__(self) -> str:
        return (
            f"<OrderItem product_id={self.product_id} "
            f"quantity={self.quantity} unit_price={self.unit_price}>"
        )