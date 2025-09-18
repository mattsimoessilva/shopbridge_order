# services/address_service.py

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

    async def CreateAsync(self, dto: AddressCreateDTO, session) -> AddressReadDTO:
        if dto is None:
            raise ValueError("Record data cannot be null.")

        entity = self._mapper.map(dto, Address)
        entity.id = uuid4()
        entity.created_at = datetime.utcnow()

        await self._repository.AddAsync(entity, session=session)
        return self._mapper.map(entity, AddressReadDTO)

    async def GetAllAsync(self, session) -> List[AddressReadDTO]:
        entities = await self._repository.GetAllAsync(session=session)
        return self._mapper.map_list(entities, AddressReadDTO) if entities else []

    async def GetByIdAsync(self, id: UUID, session) -> Optional[AddressReadDTO]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        entity = await self._repository.GetByIdAsync(id, session=session)
        return None if entity is None else self._mapper.map(entity, AddressReadDTO)

    async def UpdateAsync(self, dto: AddressUpdateDTO, session) -> bool:
        if dto is None or not dto.id:
            raise ValueError("Record data cannot be null or missing an identifier.")

        existing = await self._repository.GetByIdAsync(dto.id, session=session)
        if existing is None:
            return False

        self._mapper.map_to_existing(dto, existing)
        existing.updated_at = datetime.utcnow()

        await self._repository.UpdateAsync(existing, session=session)
        return True

    async def DeleteAsync(self, id: UUID, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        return await self._repository.DeleteAsync(id, session=session)
