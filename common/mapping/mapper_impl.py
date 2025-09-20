from typing import Any, Type, TypeVar
from common.mapping.mapper_interface import MapperInterface

T = TypeVar("T")

class Mapper(MapperInterface):
    def map(self, source: Any, target_type: Type[T]) -> T:
        target = target_type()

        # Determine the source attributes
        if isinstance(source, dict):
            source_items = source.items()
        elif hasattr(source, "__dict__"):
            source_items = vars(source).items()
        elif hasattr(source, "model_dump"):  # Pydantic v2
            source_items = source.model_dump().items()
        elif hasattr(source, "dict"):  # Pydantic v1
            source_items = source.dict().items()
        else:
            raise TypeError(f"Unsupported source type for mapping: {type(source)}")

        # Copy matching attributes
        for attr, value in source_items:
            if hasattr(target, attr):
                setattr(target, attr, value)

        return target
