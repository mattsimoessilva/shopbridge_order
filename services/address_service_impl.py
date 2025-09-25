from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from models.dtos.address.address_create_dto import AddressCreateDTO
from models.dtos.address.address_read_dto import AddressReadDTO
from models.dtos.address.address_update_dto import AddressUpdateDTO
from models.entities.address import Address
from repositories.interfaces.address_repository_interface import AddressRepositoryInterface
from services.interfaces.address_service_interface import AddressServiceInterface
from common.mapping.mapper_interface import MapperInterface


class AddressService(AddressServiceInterface):

    def __init__(self, repository: AddressRepositoryInterface):
        self._repository = repository

    async def CreateAsync(self, dto: AddressCreateDTO, session) -> AddressReadDTO:
        if dto is None:
            raise ValueError("Record data cannot be null.")
        if isinstance(dto, dict):
            dto = AddressCreateDTO(**dto)

        entity = Address(
            id=uuid4(),
            customer_id=dto.customer_id,
            street=dto.street,
            city=dto.city,
            state=dto.state,
            postal_code=dto.postal_code,
            country=dto.country,
            created_at=datetime.now(timezone.utc)
        )

        await self._repository.AddAsync(entity, session=session)

        return AddressReadDTO(
            id=entity.id,
            customer_id=entity.customer_id,
            street=entity.street,
            city=entity.city,
            state=entity.state,
            postal_code=entity.postal_code,
            country=entity.country,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    async def GetAllAsync(self, session) -> List[AddressReadDTO]:
        entities = await self._repository.GetAllAsync(session=session)
        if not entities:
            return []
        return [
            AddressReadDTO(
                id=e.id,
                customer_id=str(e.customer_id),
                street=e.street,
                city=e.city,
                state=e.state,
                postal_code=e.postal_code,
                country=e.country,
                created_at=e.created_at,
                updated_at=e.updated_at
            )
            for e in entities
        ]

    async def GetByIdAsync(self, id: UUID, session) -> Optional[AddressReadDTO]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        entity = await self._repository.GetByIdAsync(id, session=session)
        if entity is None:
            return None

        return AddressReadDTO(
            id=entity.id,
            customer_id=entity.customer_id,
            street=entity.street,
            city=entity.city,
            state=entity.state,
            postal_code=entity.postal_code,
            country=entity.country,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    async def UpdateAsync(self, dto: AddressUpdateDTO, session) -> bool:
        if dto is None or not dto.id:
            raise ValueError("Record data cannot be null or missing an identifier.")
        if isinstance(dto, dict):
            dto = AddressUpdateDTO(**dto)

        existing = await self._repository.GetByIdAsync(dto.id, session=session)
        if existing is None:
            return False

        if dto.street is not None:
            existing.street = dto.street
        if dto.city is not None:
            existing.city = dto.city
        if dto.state is not None:
            existing.state = dto.state
        if dto.postal_code is not None:
            existing.postal_code = dto.postal_code
        if dto.country is not None:
            existing.country = dto.country

        existing.updated_at = datetime.now(timezone.utc)

        await self._repository.UpdateAsync(existing, session=session)
        return True

    async def DeleteAsync(self, id: UUID, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")
        return await self._repository.DeleteAsync(id, session=session)
