from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from models.entities.address import Address


class AddressRepositoryInterface(ABC):
    @abstractmethod
    async def AddAsync(self, address: Address) -> Address:
        """Add a new Address entity to the database."""
        pass

    @abstractmethod
    async def GetAllAsync(self) -> List[Address]:
        """Retrieve all Address entities."""
        pass

    @abstractmethod
    async def GetByIdAsync(self, id: UUID) -> Optional[Address]:
        """Retrieve a single Address entity by its ID."""
        pass

    @abstractmethod
    async def GetByCustomerIdAsync(self, customer_id: UUID) -> Optional[Address]:
        """Retrive a single Address entity by its customer_id field"""
        pass

    @abstractmethod
    async def UpdateAsync(self, address: Address) -> bool:
        """Update an existing Address entity. Returns True if successful."""
        pass

    @abstractmethod
    async def DeleteAsync(self, id: UUID) -> bool:
        """Delete an Address entity by its ID. Returns True if successful."""
        pass
