from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from models.dtos.order_request_dto import OrderRequestDTO
from models.dtos.order_response_dto import OrderResponseDTO


class OrderServiceInterface(ABC):

    @abstractmethod
    async def get_all_orders_async(self) -> List[OrderResponseDTO]:
        pass

    @abstractmethod
    async def get_order_by_id_async(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        pass

    @abstractmethod
    async def create_order_async(self, dto: OrderRequestDTO) -> OrderResponseDTO:
        pass

    @abstractmethod
    async def delete_order_async(self, order_id: UUID) -> bool:
        pass

    @abstractmethod
    async def update_order_async(self, dto: OrderRequestDTO) -> bool:
        pass
