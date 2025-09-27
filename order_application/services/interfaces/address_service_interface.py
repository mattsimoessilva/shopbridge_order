from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.dtos.address import (
    AddressCreateDTO,
    AddressReadDTO,
    AddressUpdateDTO
)


class AddressServiceInterface(ABC):

    @abstractmethod
    async def CreateAsync(self, dto: AddressCreateDTO, session: AsyncSession) -> AddressReadDTO:
        """Create a new address and return the created DTO."""
        pass

    @abstractmethod
    async def GetAllAsync(self, session: AsyncSession) -> List[AddressReadDTO]:
        """Retrieve all addresses."""
        pass

    @abstractmethod
    async def GetByIdAsync(self, id: str, session: AsyncSession) -> Optional[AddressReadDTO]:
        """Retrieve a single address by its ID."""
        pass

    @abstractmethod
    async def UpdateAsync(self, id: str, dto: AddressUpdateDTO, session: AsyncSession) -> bool:
        """Update an existing address. Returns True if successful."""
        pass

    @abstractmethod
    async def DeleteAsync(self, id: str, session: AsyncSession) -> bool:
        """Delete an address by its ID. Returns True if successful."""
        pass
