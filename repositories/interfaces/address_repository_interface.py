from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from models.entities.address import Address


class AddressRepositoryInterface(ABC):
    @abstractmethod
    async def add_async(self, address: Address) -> Address:
        """Add a new Address entity to the database."""
        pass

    @abstractmethod
    async def get_all_async(self) -> List[Address]:
        """Retrieve all Address entities."""
        pass

    @abstractmethod
    async def get_by_id_async(self, id: UUID) -> Optional[Address]:
        """Retrieve a single Address entity by its ID."""
        pass

    @abstractmethod
    async def update_async(self, address: Address) -> bool:
        """Update an existing Address entity. Returns True if successful."""
        pass

    @abstractmethod
    async def delete_async(self, id: UUID) -> bool:
        """Delete an Address entity by its ID. Returns True if successful."""
        pass
