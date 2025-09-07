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

    async def create_order_async(self, order_data: dict) -> dict:
        order_id = uuid.uuid4()

        order_items = [
            OrderItem(
                id=uuid.uuid4(),
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item.get("unit_price", 0.0)
            )
            for item in order_data["items"]
        ]

        total_amount = sum(item.unit_price * item.quantity for item in order_items)

        order = Order(
            id=order_id,
            customer_id=order_data["customer_id"],
            created_at=datetime.utcnow(),
            items=order_items,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )

        await self._repository.add_async(order)

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

    async def get_all_orders_async(self) -> List[dict]:
        orders = await self._repository.get_all_async()

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

    async def get_order_by_id_async(self, order_id: UUID) -> Optional[dict]:
        order = await self._repository.get_by_id_async(order_id)
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

    async def update_order_async(self, order_data: dict) -> dict:
        existing_order = await self._repository.get_by_id_async(order_data["id"])
        if existing_order is None:
            return None

        updated_items = [
            OrderItem(
                id=uuid.uuid4(),
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item.get("unit_price", 0.0)
            )
            for item in order_data["items"]
        ]

        updated_total = sum(item.unit_price * item.quantity for item in updated_items)

        existing_order.customer_id = order_data["customer_id"]
        existing_order.created_at = datetime.utcnow()
        existing_order.items = updated_items
        existing_order.total_amount = updated_total
        existing_order.status = OrderStatus.PROCESSING

        await self._repository.update_async(existing_order)

        return {
            "id": existing_order.id,
            "created_at": existing_order.created_at,
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

    async def delete_order_async(self, order_id: UUID) -> bool:
        return await self._repository.remove_async(order_id)
