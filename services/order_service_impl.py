import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from models.dtos.order_create_dto import OrderCreateDTO
from models.dtos.order_read_dto import OrderReadDTO
from models.dtos.order_update_dto import OrderUpdateDTO
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.enums.order_status import OrderStatus
from repositories.interfaces.order_repository_interface import OrderRepositoryInterface
from services.interfaces.order_service_interface import OrderServiceInterface
from services.mapping.mapper_interface import MapperInterface


class OrderService(OrderServiceInterface):

    def __init__(self, repository: OrderRepositoryInterface, mapper: MapperInterface):
        self._repository = repository
        self._mapper = mapper


    async def create_async(self, dto: OrderCreateDTO) -> OrderReadDTO:
        if dto is None:
            raise ValueError("The provided record data cannot be null.")

        entity = self._mapper.map(dto, Order)
        entity.id = uuid.uuid4()
        entity.created_at = datetime.utcnow()
        entity.status = OrderStatus.PENDING

        # Calculate total amount
        entity.total_amount = sum(
            item.unit_price * item.quantity for item in entity.items
        )

        await self._repository.add_async(entity)

        return self._mapper.map(entity, OrderReadDTO)


    async def get_all_async(self) -> List[OrderReadDTO]:
        entities = await self._repository.get_all_async()

        if not entities:
            return []

        return self._mapper.map_list(entities, OrderReadDTO)


    async def get_by_id_async(self, id: UUID) -> Optional[OrderReadDTO]:
        if not id:
            raise ValueError("The provided record identifier cannot be empty.")

        entity = await self._repository.get_by_id_async(id)

        if entity is None:
            return None

        return self._mapper.map(entity, OrderReadDTO)


    async def update_async(self, dto: OrderUpdateDTO) -> bool:
        if dto is None or not dto.id:
            raise ValueError("The provided record data cannot be null or missing an identifier.")

        existing = await self._repository.get_by_id_async(dto.id)

        if existing is None:
            return False

        self._mapper.map_to_existing(dto, existing)

        # Recalculate total if items changed
        if dto.items:
            existing.total_amount = sum(
                item.unit_price * item.quantity for item in existing.items
            )

        existing.updated_at = datetime.utcnow()

        await self._repository.update_async(existing)

        return True


    async def delete_async(self, id: UUID) -> bool:
        if not id:
            raise ValueError("The provided record identifier cannot be empty.")

        return await self._repository.delete_async(id)
