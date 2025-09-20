import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_read_dto import OrderReadDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO
from models.dtos.order_item.order_item_read_dto import OrderItemReadDTO
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.enums.order_status import OrderStatus
from repositories.interfaces.order_repository_interface import OrderRepositoryInterface
from services.interfaces.order_service_interface import OrderServiceInterface
from common.mapping.mapper_interface import MapperInterface


class OrderService(OrderServiceInterface):

    def __init__(self, repository: OrderRepositoryInterface, mapper: MapperInterface):
        self._repository = repository
        self._mapper = mapper

    async def CreateAsync(self, dto: OrderCreateDTO, session) -> OrderReadDTO:
        if dto is None:
            raise ValueError("Record data cannot be null.")
        if isinstance(dto, dict):
            dto = OrderCreateDTO(**dto)

        entity = Order(
            id=uuid.uuid4(),
            customer_id=dto.customer_id,
            created_at=datetime.now(timezone.utc),
            status=OrderStatus.PENDING,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price
                )
                for item in dto.items
            ]
        )
        entity.total_amount = sum(Decimal(item.unit_price) * item.quantity for item in entity.items)

        await self._repository.AddAsync(entity, session=session)

        return OrderReadDTO(
            id=entity.id,
            created_at=entity.created_at,
            customer_id=entity.customer_id,
            total_amount=entity.total_amount,
            status=entity.status,
            items=[
                OrderItemReadDTO(
                    id=item.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.unit_price * item.quantity
                )
                for item in entity.items
            ]
        )

    async def GetAllAsync(self, session) -> List[OrderReadDTO]:
        entities = await self._repository.GetAllAsync(session=session)
        if not entities:
            return []
        return [
            OrderReadDTO(
                id=e.id,
                created_at=e.created_at,
                customer_id=e.customer_id,
                total_amount=e.total_amount,
                status=e.status,
                items=[
                    OrderItemReadDTO(
                        id=i.id,
                        product_id=i.product_id,
                        quantity=i.quantity,
                        unit_price=i.unit_price,
                        total_price=i.unit_price * i.quantity
                    )
                    for i in e.items
                ]
            )
            for e in entities
        ]

    async def GetByIdAsync(self, id: UUID, session) -> Optional[OrderReadDTO]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        entity = await self._repository.GetByIdAsync(id, session=session)
        if entity is None:
            return None

        return OrderReadDTO(
            id=entity.id,
            created_at=entity.created_at,
            customer_id=entity.customer_id,
            total_amount=entity.total_amount,
            status=entity.status,
            items=[
                OrderItemReadDTO(
                    id=item.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.unit_price * item.quantity
                )
                for item in entity.items
            ]
        )

    async def UpdateAsync(self, dto: OrderUpdateDTO, session) -> bool:
        if dto is None or not dto.id:
            raise ValueError("Record data cannot be null or missing an identifier.")
        if isinstance(dto, dict):
            dto = OrderUpdateDTO(**dto)

        existing = await self._repository.GetByIdAsync(dto.id, session=session)
        if existing is None:
            return False

        if dto.customer_id is not None:
            existing.customer_id = dto.customer_id
        if dto.status is not None:
            existing.status = dto.status
        if dto.items is not None:
            existing.items = [
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price
                )
                for item in dto.items
            ]
            existing.total_amount = sum(
                Decimal(item.unit_price) * item.quantity for item in existing.items
            )

        existing.updated_at = datetime.now(timezone.utc)
        await self._repository.UpdateAsync(existing, session=session)
        return True

    async def DeleteAsync(self, id: UUID, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")
        return await self._repository.DeleteAsync(id, session=session)
