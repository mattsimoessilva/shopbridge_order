# common/mapping/mapper_interface.py
from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

T = TypeVar("T")

class MapperInterface(ABC):
    @abstractmethod
    def map(self, source: Any, target_type: Type[T]) -> T:
        pass
