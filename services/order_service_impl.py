import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.enums.order_status import OrderStatus
from repositories.interfaces.order_repository_interface import OrderRepositoryInterface
from services.interfaces.order_service_interface import OrderServiceInterface

class OrderService(OrderServiceInterface):
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    def create_order(self, order_data: dict) -> dict:
        order_id = uuid.uuid4()

        items_data = order_data.get("items", [])
        order_items = [
            OrderItem(
                id=uuid.uuid4(),
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item.get("unit_price", 0.0)
            )
            for item in items_data
        ]


        total_amount = sum(item.unit_price * item.quantity for item in order_items)

        order = Order(
            id=order_id,
            customer_id = order_data.get("customer_id"),
            created_at=datetime.utcnow(),
            items=order_items,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )

        self._repository.add(order)

        return {
            "id": order.id,
            "created_at": order.created_at,
            "customer_id": order.customer_id,
            "status": order.status.value,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in order.items
            ],
            "total_amount": order.total_amount
        }

    def get_all_orders(self) -> List[dict]:
        orders = self._repository.get_all()

        return [
            {
                "id": order.id,
                "created_at": order.created_at,
                "customer_id": order.customer_id,
                "status": order.status.value,
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price
                    }
                    for item in order.items
                ],
                "total_amount": order.total_amount
            }
            for order in orders
        ]

    def get_order_by_id(self, order_id: UUID) -> Optional[dict]:
        order = self._repository.get_by_id(order_id)
        if order is None:
            return None

        return {
            "id": order.id,
            "created_at": order.created_at,
            "customer_id": order.customer_id,
            "status": order.status.value,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in order.items
            ],
            "total_amount": order.total_amount
        }

    def update_order(self, order_data: dict) -> dict:
        existing_order = self._repository.get_by_id(order_data["id"])
        if existing_order is None:
            return None

        if "status" in order_data:
            existing_order.status = OrderStatus(order_data["status"])

        items_data = order_data.get("items")
        if items_data:
            updated_items = [
                OrderItem(
                    id=uuid.uuid4(),
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    unit_price=item.get("unit_price", 0.0)
                )
                for item in items_data
            ]
            existing_order.items = updated_items
            existing_order.total_amount = sum(item.unit_price * item.quantity for item in updated_items)

        # Update deleted_at if provided
        if "deleted_at" in order_data:
            existing_order.deleted_at = order_data["deleted_at"]

        # Never update customer_id or created_at
        existing_order.updated_at = datetime.utcnow()

        self._repository.update(existing_order)

        return {
            "id": existing_order.id,
            "created_at": existing_order.created_at,
            "updated_at": existing_order.updated_at,
            "customer_id": existing_order.customer_id,
            "status": existing_order.status.value,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in existing_order.items
            ],
            "total_amount": existing_order.total_amount
        }

    def delete_order(self, order_id: UUID) -> bool:
        return self._repository.remove(order_id)
