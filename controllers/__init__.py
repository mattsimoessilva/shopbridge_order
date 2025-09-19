# controllers/__init__.py

from .order_controller import blp as order_blp
from .address_controller import blp as address_blp

__all__ = ["order_blp", "address_blp"]
