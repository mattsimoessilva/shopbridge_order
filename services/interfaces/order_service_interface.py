from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from models.dtos.order_create_dto import OrderCreateDTO
from models.dtos.order_read_dto import OrderReadDTO
from models.dtos.order_update_dto import OrderUpdateDTO


class OrderServiceInterface(ABC):

    @abstractmethod
    async def create_async(self, dto: OrderCreateDTO) -> OrderReadDTO:
        """Create a new record and return its read representation."""
        pass


    @abstractmethod
    async def get_all_async(self) -> List[OrderReadDTO]:
        """Retrieve all records."""
        pass


    @abstractmethod
    async def get_by_id_async(self, id: UUID) -> Optional[OrderReadDTO]:
        """Retrieve a specific record by its identifier."""
        pass


    @abstractmethod
    async def update_async(self, dto: OrderUpdateDTO) -> bool:
        """Update an existing record. Returns True if successful."""
        pass


    @abstractmethod
    async def delete_async(self, id: UUID) -> bool:
        """Delete a record by its identifier. Returns True if successful."""
        pass
