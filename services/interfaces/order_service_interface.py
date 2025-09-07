from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID


class OrderServiceInterface(ABC):

    @abstractmethod
    def get_all_orders(self) -> List[dict]:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: UUID) -> Optional[dict]:
        pass

    @abstractmethod
    def create_order(self, order_data: dict) -> dict:
        pass

    @abstractmethod
    def delete_order(self, order_id: UUID) -> bool:
        pass

    @abstractmethod
    def update_order(self, order_data: dict) -> dict:
        pass
