from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update as sql_update, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from models.entities.order import Order
from repositories.order_repository_interface import OrderRepositoryInterface


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, async_session: AsyncSession, sync_session: Session):
        self._async_session = async_session
        self._sync_session = sync_session

    async def get_all_async(self) -> List[Order]:
        stmt = (
            select(Order)
            .where(Order.deleted_at.is_(None))
            .options(selectinload(Order.items))
        )

        result = await self._async_session.execute(stmt)

        return result.scalars().all()

    async def get_by_id_async(self, order_id: UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items))
        )

        result = await self._async_session.execute(stmt)

        return result.scalars().first()

    async def add_async(self, order: Order) -> None:
        self._async_session.add(order)

        await self._async_session.commit()

    async def remove_async(self, order_id: UUID) -> bool:
        stmt = select(Order).where(Order.id == order_id)
        result = await self._async_session.execute(stmt)
        order = result.scalars().first()

        if order is None:
            return False

        await self._async_session.delete(order)
        await self._async_session.commit()

        return True

    async def update_async(self, updated_order: Order) -> bool:
        stmt = select(Order).where(Order.id == updated_order.id)
        result = await self._async_session.execute(stmt)
        existing_order = result.scalars().first()

        if existing_order is None:
            return False

        existing_order.customer_id = updated_order.customer_id
        existing_order.items = updated_order.items

        await self._async_session.commit()

        return True

  