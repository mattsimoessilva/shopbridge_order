from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from logistics_api.models.dtos.address import (
    AddressCreateDTO,
    AddressReadDTO,
    AddressUpdateDTO
)

class AddressServiceInterface(ABC):
    @abstractmethod
    async def create_async(self, dto: AddressCreateDTO) -> AddressReadDTO:
        """Create a new address and return the created DTO."""
        pass

    @abstractmethod
    async def get_all_async(self) -> List[AddressReadDTO]:
        """Retrieve all addresses."""
        pass

    @abstractmethod
    async def get_by_id_async(self, id: UUID) -> Optional[AddressReadDTO]:
        """Retrieve a single address by its ID."""
        pass

    @abstractmethod
    async def update_async(self, dto: AddressUpdateDTO) -> bool:
        """Update an existing address. Returns True if successful."""
        pass

    @abstractmethod
    async def delete_async(self, id: UUID) -> bool:
        """Delete an address by its ID. Returns True if successful."""
        pass
