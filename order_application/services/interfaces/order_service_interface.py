from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_read_dto import OrderReadDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO
from models.dtos.order.order_patch_dto import OrderPatchDTO


class OrderServiceInterface(ABC):

    @abstractmethod
    async def CreateAsync(self, dto: OrderCreateDTO, session: AsyncSession) -> OrderReadDTO:
        """Create a new record and return its read representation."""
        pass

    @abstractmethod
    async def GetAllAsync(self, session: AsyncSession) -> List[OrderReadDTO]:
        """Retrieve all records."""
        pass

    @abstractmethod
    async def GetByIdAsync(self, id: str, session: AsyncSession) -> Optional[OrderReadDTO]:
        """Retrieve a specific record by its identifier."""
        pass

    @abstractmethod
    async def UpdateAsync(self, id: str, dto: OrderUpdateDTO, session: AsyncSession) -> bool:
        """Update an existing record. Returns True if successful."""
        pass

    @abstractmethod
    async def DeleteAsync(self, id: str, session: AsyncSession) -> bool:
        """Delete a record by its identifier. Returns True if successful."""
        pass

    @abstractmethod
    async def PatchAsync(self, id: str, dto: OrderPatchDTO, session: AsyncSession) -> bool:
        """Patches a record by its identifier. Returns True if successful."""
        pass
