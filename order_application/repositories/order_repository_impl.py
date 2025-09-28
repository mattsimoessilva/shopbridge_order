from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.entities import Order
from repositories.interfaces import OrderRepositoryInterface
from datetime import datetime, timezone

class OrderRepository(OrderRepositoryInterface):

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def AddAsync(self, entity: Order, session: AsyncSession) -> Order:
        if entity is None:
            raise ValueError("Record reference cannot be null.")

        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    async def GetAllAsync(self, session: AsyncSession) -> List[Order]:
        result = await session.execute(select(Order))
        return result.scalars().all()

    async def GetByIdAsync(self, id: str, session: AsyncSession) -> Optional[Order]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        result = await session.execute(
            select(Order).where(Order.id == id)
        )
        return result.scalars().first()

    async def UpdateAsync(self, updated: Order, session: AsyncSession) -> Order | None:
        if updated is None:
            raise ValueError("Record data cannot be null.")

        existing = await self.GetByIdAsync(updated.id, session=session)
        if existing is None:
            return None

        existing.shipment_id = updated.shipment_id
        existing.items = updated.items

        existing.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(existing)
        return existing

    async def DeleteAsync(self, id: str, session: AsyncSession) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        existing = await self.GetByIdAsync(id, session=session)
        if existing is None:
            return False

        await session.delete(existing)
        await session.commit()
        return True
