# services/order_service.py

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

    async def CreateAsync(self, dto: OrderCreateDTO, session) -> OrderReadDTO:
        if dto is None:
            raise ValueError("Record data cannot be null.")

        entity = self._mapper.map(dto, Order)
        entity.id = uuid.uuid4()
        entity.created_at = datetime.utcnow()
        entity.status = OrderStatus.PENDING
        entity.total_amount = sum(
            item.unit_price * item.quantity for item in (entity.items or [])
        )

        await self._repository.AddAsync(entity, session=session)
        return self._mapper.map(entity, OrderReadDTO)

    async def GetAllAsync(self, session) -> List[OrderReadDTO]:
        entities = await self._repository.GetAllAsync(session=session)
        return self._mapper.map_list(entities, OrderReadDTO) if entities else []

    async def GetByIdAsync(self, id: UUID, session) -> Optional[OrderReadDTO]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        entity = await self._repository.GetByIdAsync(id, session=session)
        return None if entity is None else self._mapper.map(entity, OrderReadDTO)

    async def UpdateAsync(self, dto: OrderUpdateDTO, session) -> bool:
        if dto is None or not dto.id:
            raise ValueError("Record data cannot be null or missing an identifier.")

        existing = await self._repository.GetByIdAsync(dto.id, session=session)
        if existing is None:
            return False

        self._mapper.map_to_existing(dto, existing)

        if dto.items:
            existing.total_amount = sum(
                item.unit_price * item.quantity for item in existing.items
            )

        existing.updated_at = datetime.utcnow()
        await self._repository.UpdateAsync(existing, session=session)

        return True

    async def DeleteAsync(self, id: UUID, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        return await self._repository.DeleteAsync(id, session=session)
