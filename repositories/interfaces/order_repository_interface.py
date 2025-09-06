from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from models.entities.order import Order


class OrderRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_async(self) -> List[Order]:
        pass

    @abstractmethod
    async def get_by_id_async(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    async def add_async(self, order: Order) -> None:
        pass

    @abstractmethod
    async def remove_async(self, order_id: UUID) -> bool:
        pass

    @abstractmethod
    async def update_async(self, order: Order) -> bool:
        pass
