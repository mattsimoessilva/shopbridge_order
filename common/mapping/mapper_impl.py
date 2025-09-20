# common/mapping/mapper_impl.py
from typing import Any, Type, TypeVar
from common.mapping.mapper_interface import MapperInterface

T = TypeVar("T")

class Mapper(MapperInterface):
    def map(self, source: Any, target_type: Type[T]) -> T:
        target = target_type()
        for attr, value in vars(source).items():
            if hasattr(target, attr):
                setattr(target, attr, value)
        return target
