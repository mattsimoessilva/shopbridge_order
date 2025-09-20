from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from models.dtos.address import (
    AddressCreateDTO,
    AddressReadDTO,
    AddressUpdateDTO
)

class AddressServiceInterface(ABC):
    @abstractmethod
    async def CreateAsync(self, dto: AddressCreateDTO) -> AddressReadDTO:
        """Create a new address and return the created DTO."""
        pass

    @abstractmethod
    async def GetAllAsync(self) -> List[AddressReadDTO]:
        """Retrieve all addresses."""
        pass

    @abstractmethod
    async def GetByIdAsync(self, id: UUID) -> Optional[AddressReadDTO]:
        """Retrieve a single address by its ID."""
        pass

    @abstractmethod
    async def UpdateAsync(self, dto: AddressUpdateDTO) -> bool:
        """Update an existing address. Returns True if successful."""
        pass

    @abstractmethod
    async def DeleteAsync(self, id: UUID) -> bool:
        """Delete an address by its ID. Returns True if successful."""
        pass
