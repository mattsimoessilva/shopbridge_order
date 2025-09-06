import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from models.dtos.order_request_dto import OrderRequestDTO
from models.dtos.order_response_dto import OrderResponseDTO
from models.dtos.order_item_dto import OrderItemDTO
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.entities.order_status import OrderStatus
from services.order_service_interface import OrderServiceInterface
from repositories.order_repository_interface import OrderRepositoryInterface


class OrderService(OrderServiceInterface):
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    async def create_order_async(self, dto: OrderRequestDTO) -> OrderResponseDTO:
        order_id = uuid.uuid4()

        order_items = [
            OrderItem(
                id=uuid.uuid4(),
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            for item in dto.items
        ]

        total_amount = sum(p.unit_price * p.quantity for p in order_items)

        order = Order(
            id=order_id,
            customer_id=dto.customer_id,
            created_at=datetime.utcnow(),
            items=order_items,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )

        await self._repository.add_async(order)

        return OrderResponseDTO(
            id=order.id,
            created_at=order.created_at,
            customer_id=order.customer_id,
            status=order.status,
            items=[
                OrderItemDTO(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    quantity=i.quantity,
                    unit_price=i.unit_price
                )
                for i in order.items
            ],
            total_amount=order.total_amount
        )

    async def get_all_orders_async(self) -> List[OrderResponseDTO]:
        orders = await self._repository.get_all_async()

        return [
            OrderResponseDTO(
                id=order.id,
                created_at=order.created_at,
                customer_id=order.customer_id,
                status=order.status,
                items=[
                    OrderItemDTO(
                        product_id=item.product_id,
                        product_name=item.product_name,
                        quantity=item.quantity,
                        unit_price=item.unit_price
                    )
                    for item in order.items
                ],
                total_amount=order.total_amount
            )
            for order in orders
        ]

    async def get_order_by_id_async(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        order = await self._repository.get_by_id_async(order_id)
        if order is None:
            return None

        return OrderResponseDTO(
            id=order.id,
            created_at=order.created_at,
            customer_id=order.customer_id,
            status=order.status,
            items=[
                OrderItemDTO(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    quantity=i.quantity,
                    unit_price=i.unit_price
                )
                for i in order.items
            ],
            total_amount=order.total_amount
        )

    async def update_order_async(self, dto: OrderRequestDTO) -> bool:
        existing_order = await self._repository.get_by_id_async(dto.id)
        if existing_order is None:
            return False

        updated_items = [
            OrderItem(
                id=uuid.uuid4(),
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            for item in dto.items
        ]

        updated_total = sum(i.unit_price * i.quantity for i in updated_items)

        existing_order.customer_id = dto.customer_id
        existing_order.created_at = datetime.utcnow()
        existing_order.items = updated_items
        existing_order.total_amount = updated_total
        existing_order.status = OrderStatus.PROCESSING

        await self._repository.update_async(existing_order)
        return True

    async def delete_order_async(self, order_id: UUID) -> bool:
        return await self._repository.remove_async(order_id)
