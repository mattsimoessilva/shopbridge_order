from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from models.entities.order import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    async def AddAsync(self, address: Order) -> Order:
        """Add a new Order entity to the database."""
        pass

    @abstractmethod
    async def GetAllAsync(self) -> List[Order]:
        """Retrieve all Order entities."""
        pass

    @abstractmethod
    async def GetByIdAsync(self, id: UUID) -> Optional[Order]:
        """Retrieve a single Order entity by its ID."""
        pass

    @abstractmethod
    async def UpdateAsync(self, address: Order) -> bool:
        """Update an existing Order entity. Returns True if successful."""
        pass

    @abstractmethod
    async def DeleteAsync(self, id: UUID) -> bool:
        """Delete an Order entity by its ID. Returns True if successful."""
        pass
