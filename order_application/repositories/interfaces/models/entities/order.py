import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, Numeric, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.entities.base import Base
from models.enums import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=datetime.utcnow
    )

    customer_id: Mapped[str] = mapped_column(String(36), nullable=False)

    shipment_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    total_amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=2), nullable=False
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.PENDING
    )

    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} customer_id={self.customer_id} status={self.status}>"
