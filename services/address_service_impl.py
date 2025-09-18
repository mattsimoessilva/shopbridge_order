from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from models.dtos.address_create_dto import AddressCreateDTO
from models.dtos.address_read_dto import AddressReadDTO
from models.dtos.address_update_dto import AddressUpdateDTO
from models.entities.address import Address
from repositories.interfaces.address_repository_interface import AddressRepositoryInterface
from services.interfaces.address_service_interface import AddressServiceInterface
from services.mapping.mapper_interface import MapperInterface  # Similar to AutoMapper


class AddressService(AddressServiceInterface):
    def __init__(self, repository: AddressRepositoryInterface, mapper: MapperInterface):
        self._repository = repository
        self._mapper = mapper

    async def create_async(self, dto: AddressCreateDTO) -> AddressReadDTO:
        if dto is None:
            raise ValueError("DTO cannot be None")

        entity = self._mapper.map(dto, Address)
        entity.id = uuid4()
        entity.created_at = datetime.utcnow()

        await self._repository.add_async(entity)

        return self._mapper.map(entity, AddressReadDTO)

    async def get_all_async(self) -> List[AddressReadDTO]:
        entities = await self._repository.get_all_async()

        if not entities:
            return []

        return self._mapper.map_list(entities, AddressReadDTO)

    async def get_by_id_async(self, id: UUID) -> Optional[AddressReadDTO]:
        if not id:
            raise ValueError("Invalid ID")

        entity = await self._repository.get_by_id_async(id)

        if entity is None:
            return None

        return self._mapper.map(entity, AddressReadDTO)

    async def update_async(self, dto: AddressUpdateDTO) -> bool:
        if dto is None or not dto.id:
            raise ValueError("Invalid update data")

        existing = await self._repository.get_by_id_async(dto.id)
        if existing is None:
            return False

        self._mapper.map_to_existing(dto, existing)
        existing.updated_at = datetime.utcnow()

        await self._repository.update_async(existing)
        return True

    async def delete_async(self, id: UUID) -> bool:
        if not id:
            raise ValueError("Invalid ID")

        await self._repository.delete_async(id)
        return True
