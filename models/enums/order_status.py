from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "Pending"        # Order has been created but not yet processed
    PROCESSING = "Processing"  # Order is currently being processed
    SHIPPED = "Shipped"        # Order has been shipped to the customer
    DELIVERED = "Delivered"    # Order has been delivered to the customer
    CANCELLED = "Cancelled"    # Order has been cancelled

    def __str__(self) -> str:
        return self.value
