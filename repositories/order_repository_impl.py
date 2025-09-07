from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update as sql_update, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from models.entities.order import Order
from repositories.interfaces.order_repository_interface import OrderRepositoryInterface


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, sync_session: Session):
        self._sync_session = sync_session

    def get_all(self) -> List[Order]:
        stmt = (
            select(Order)
            .where(Order.deleted_at.is_(None))
            .options(selectinload(Order.items))
        )

        result = self._sync_session.execute(stmt)

        return result.scalars().all()

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items))
        )

        result = self._sync_session.execute(stmt)

        return result.scalars().first()

    def add(self, order: Order) -> None:
        self._sync_session.add(order)

        self._sync_session.commit()

    def remove(self, order_id: UUID) -> bool:
        stmt = select(Order).where(Order.id == order_id)
        result = self._sync_session.execute(stmt)
        order = result.scalars().first()

        if order is None:
            return False

        self._sync_session.delete(order)
        self._sync_session.commit()

        return True

    def update(self, updated_order: Order) -> bool:
        stmt = select(Order).where(Order.id == updated_order.id)
        result = self._sync_session.execute(stmt)
        existing_order = result.scalars().first()

        if existing_order is None:
            return False

        existing_order.customer_id = updated_order.customer_id
        existing_order.items = updated_order.items

        self._sync_session.commit()

        return True

  