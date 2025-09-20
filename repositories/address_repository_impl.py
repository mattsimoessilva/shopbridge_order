# repositories/address_repository.py

from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.entities.address import Address
from repositories.interfaces.address_repository_interface import AddressRepositoryInterface
from common.mapping.mapper_interface import MapperInterface


class AddressRepository(AddressRepositoryInterface):

    def __init__(self, session_factory, mapper):
        self._session_factory = session_factory
        self._mapper = mapper


    async def AddAsync(self, entity: Address, session: AsyncSession) -> Address:
        if entity is None:
            raise ValueError("Record reference cannot be null.")

        session.add(entity)
        await session.commit()
        await session.refresh(entity)

        return entity

    async def GetAllAsync(self, session: AsyncSession) -> List[Address]:
        result = await session.execute(select(Address))
        return result.scalars().all()

    async def GetByIdAsync(self, id: UUID, session: AsyncSession) -> Optional[Address]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        result = await session.execute(
            select(Address).where(Address.id == id)
        )
        return result.scalars().first()

    async def UpdateAsync(self, updated: Address, session: AsyncSession) -> bool:
        if updated is None:
            raise ValueError("Record data cannot be null.")

        existing = await self.GetByIdAsync(updated.id, session=session)
        if existing is None:
            return False

        self._mapper.map(updated, existing)
        await session.commit()

        return True

    async def DeleteAsync(self, id: UUID, session: AsyncSession) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        existing = await self.GetByIdAsync(id, session=session)
        if existing is None:
            return False

        await session.delete(existing)
        await session.commit()

        return True
