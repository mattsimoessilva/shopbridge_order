from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from models.entities.order import Order

class OrderRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> List[Order]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def add(self, order: Order) -> None:
        pass

    @abstractmethod
    def remove(self, order_id: UUID) -> bool:
        pass

    @abstractmethod
    def update(self, order: Order) -> bool:
        pass
