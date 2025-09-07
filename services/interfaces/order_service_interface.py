from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID


class OrderServiceInterface(ABC):

    @abstractmethod
    async def get_all_orders_async(self) -> List[dict]:
        """Returns a list of orders matching OrderResponseSchema"""
        pass

    @abstractmethod
    async def get_order_by_id_async(self, order_id: UUID) -> Optional[dict]:
        """Returns a single order matching OrderResponseSchema"""
        pass

    @abstractmethod
    async def create_order_async(self, order_data: dict) -> dict:
        """Accepts validated data matching OrderRequestSchema and returns OrderResponseSchema"""
        pass

    @abstractmethod
    async def delete_order_async(self, order_id: UUID) -> bool:
        """Deletes an order by ID"""
        pass

    @abstractmethod
    async def update_order_async(self, order_data: dict) -> dict:
        """Accepts validated data matching OrderRequestSchema and returns updated OrderResponseSchema"""
        pass
