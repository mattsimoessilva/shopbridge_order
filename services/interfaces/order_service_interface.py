from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_read_dto import OrderReadDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO


class OrderServiceInterface(ABC):

    @abstractmethod
    async def CreateAsync(self, dto: OrderCreateDTO) -> OrderReadDTO:
        """Create a new record and return its read representation."""
        pass


    @abstractmethod
    async def GetAllAsync(self) -> List[OrderReadDTO]:
        """Retrieve all records."""
        pass


    @abstractmethod
    async def GetByIdAsync(self, id: UUID) -> Optional[OrderReadDTO]:
        """Retrieve a specific record by its identifier."""
        pass


    @abstractmethod
    async def UpdateAsync(self, dto: OrderUpdateDTO) -> bool:
        """Update an existing record. Returns True if successful."""
        pass


    @abstractmethod
    async def DeleteAsync(self, id: UUID) -> bool:
        """Delete a record by its identifier. Returns True if successful."""
        pass
