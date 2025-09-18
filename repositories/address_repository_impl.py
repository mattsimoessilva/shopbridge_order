from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.entities.address import Address
from repositories.interfaces.address_repository_interface import AddressRepositoryInterface
from services.mapping.mapper_interface import MapperInterface


class AddressRepository(AddressRepositoryInterface):

    def __init__(self, session: AsyncSession, mapper: MapperInterface):
        self._session = session
        self._mapper = mapper


    async def add_async(self, entity: Address) -> Address:
        if entity is None:
            raise ValueError("The provided record reference cannot be null.")

        self._session.add(entity)

        await self._session.commit()
        await self._session.refresh(entity)

        return entity


    async def get_all_async(self) -> List[Address]:
        result = await self._session.execute(
            select(Address)
        )

        return result.scalars().all()


    async def get_by_id_async(self, id: UUID) -> Optional[Address]:
        if not id:
            raise ValueError("The provided record identifier cannot be empty.")

        result = await self._session.execute(
            select(Address).where(Address.id == id)
        )

        return result.scalars().first()


    async def update_async(self, updated: Address) -> bool:
        if updated is None:
            raise ValueError("The provided record data cannot be null.")

        existing = await self.get_by_id_async(updated.id)

        if existing is None:
            return False

        self._mapper.map(updated, existing)

        await self._session.commit()

        return True


    async def delete_async(self, id: UUID) -> bool:
        if not id:
            raise ValueError("The provided record identifier cannot be empty.")

        existing = await self.get_by_id_async(id)

        if existing is None:
            return False

        await self._session.delete(existing)
        await self._session.commit()

        return True
