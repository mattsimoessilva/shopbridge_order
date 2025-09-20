import pytest
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from services.address_service_impl import AddressService
from models.entities.address import Address
from models.dtos.address.address_create_dto import AddressCreateDTO
from models.dtos.address.address_read_dto import AddressReadDTO
from models.dtos.address.address_update_dto import AddressUpdateDTO


@pytest.fixture
def service_with_mocks():
    repo_mock = AsyncMock()
    mapper_mock = MagicMock()
    service = AddressService(repo_mock, mapper_mock)
    return service, repo_mock, mapper_mock


# region CreateAsync Method.

@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseValueError_WhenDTOIsNone(service_with_mocks):
    # Arrange
    service, repo_mock, mapper_mock = service_with_mocks
    dto = None

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        await service.CreateAsync(dto, session="session")
    assert "cannot be null" in str(exc_info.value)
    mapper_mock.map.assert_not_called()
    repo_mock.AddAsync.assert_not_called()


@pytest.mark.asyncio
async def test_CreateAsync_ShouldReturnDTO_WhenDTOIsValid(service_with_mocks):
    # Arrange
    service, repo_mock, mapper_mock = service_with_mocks
    create_dto = AddressCreateDTO(
        street="123 Main St", city="NY", state="NY", postal_code="10001", country="USA"
    )
    entity = Address()
    read_dto = AddressReadDTO(
        id=uuid.uuid4(),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA",
        created_at=datetime.now(timezone.utc)
    )

    mapper_mock.map.side_effect = [entity, read_dto]

    # Act
    result = await service.CreateAsync(create_dto, session="session")

    # Assert
    assert result == read_dto
    repo_mock.AddAsync.assert_awaited_once_with(entity, session="session")
    mapper_mock.map.assert_any_call(create_dto, Address)
    mapper_mock.map.assert_any_call(entity, AddressReadDTO)


@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    # Arrange
    service, repo_mock, mapper_mock = service_with_mocks
    create_dto = AddressCreateDTO(
        street="123 Main St", city="NY", state="NY", postal_code="10001", country="USA"
    )
    entity = Address()
    mapper_mock.map.return_value = entity
    repo_mock.AddAsync.side_effect = Exception("Repository failure.")

    # Act / Assert
    with pytest.raises(Exception) as exc_info:
        await service.CreateAsync(create_dto, session="session")
    assert "Repository failure." in str(exc_info.value)
    repo_mock.AddAsync.assert_awaited_once_with(entity, session="session")

# endregion


# region GetAllAsync Method.

@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnList_WhenRecordsExist(service_with_mocks):
    # Arrange
    service, repo_mock, mapper_mock = service_with_mocks
    entities = [Address(), Address()]
    repo_mock.GetAllAsync.return_value = entities
    expected_dtos = [
        AddressReadDTO(
            id=uuid.uuid4(),
            street="123 Main St",
            city="NY",
            state="NY",
            postal_code="10001",
            country="USA",
            created_at=datetime.now(timezone.utc)
        ),
        AddressReadDTO(
            id=uuid.uuid4(),
            street="456 Elm St",
            city="Boston",
            state="MA",
            postal_code="02118",
            country="USA",
            created_at=datetime.now(timezone.utc)
        )
    ]
    mapper_mock.map_list.return_value = expected_dtos

    # Act
    result = await service.GetAllAsync(session="session")

    # Assert
    assert result == expected_dtos
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")
    mapper_mock.map_list.assert_called_once_with(entities, AddressReadDTO)


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnEmptyList_WhenNoRecordsExist(service_with_mocks):
    # Arrange
    service, repo_mock, _ = service_with_mocks
    repo_mock.GetAllAsync.return_value = None

    # Act
    result = await service.GetAllAsync(session="session")

    # Assert
    assert result == []
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")

# endregion


# region GetByIdAsync Method.

@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    # Arrange
    service, _, _ = service_with_mocks

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        await service.GetByIdAsync(None, session="session")
    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnDTO_WhenRecordExists(service_with_mocks):
    # Arrange
    service, repo_mock, mapper_mock = service_with_mocks
    address_id = uuid.uuid4()
    entity = Address()
    expected_dto = AddressReadDTO(
        id=address_id,
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA",
        created_at=datetime.now(timezone.utc)
    )
    repo_mock.GetByIdAsync.return_value = entity
    mapper_mock.map.return_value = expected_dto

    # Act
    result = await service.GetByIdAsync(address_id, session="session")

    # Assert
    assert result == expected_dto
    repo_mock.GetByIdAsync.assert_awaited_once_with(address_id, session="session")
    mapper_mock.map.assert_called_once_with(entity, AddressReadDTO)


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnNone_WhenRecordDoesNotExist(service_with_mocks):
    # Arrange
    service, repo_mock, _ = service_with_mocks
    address_id = uuid.uuid4()
    repo_mock.GetByIdAsync.return_value = None

    # Act
    result = await service.GetByIdAsync(address_id, session="session")

    # Assert
    assert result is None
    repo_mock.GetByIdAsync.assert_awaited_once_with(address_id, session="session")

# endregion


# region UpdateAsync Method.

@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseValueError_WhenDTOIsInvalid(service_with_mocks):
    # Arrange
    service, _, _ = service_with_mocks

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        await service.UpdateAsync(None, session="session")
    assert "cannot be null" in str(exc_info.value)


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnFalse_WhenRecordDoesNotExist(service_with_mocks):
    # Arrange
    service, repo_mock, _ = service_with_mocks
    dto = AddressUpdateDTO(
        id=uuid.uuid4(),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    repo_mock.GetByIdAsync.return_value = None

    # Act
    result = await service.UpdateAsync(dto, session="session")

    # Assert
    assert result is False
    repo_mock.GetByIdAsync.assert_awaited_once_with(dto.id, session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnTrue_WhenUpdateSucceeds(service_with_mocks):
    # Arrange
    service, repo_mock, mapper_mock = service_with_mocks
    dto = AddressUpdateDTO(
        id=uuid.uuid4(),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    existing = Address()
    repo_mock.GetByIdAsync.return_value = existing

    # Act
    result = await service.UpdateAsync(dto, session="session")

    # Assert
    assert result is True
    mapper_mock.map_to_existing.assert_called_once_with(dto, existing)
    repo_mock.UpdateAsync.assert_awaited_once_with(existing, session="session")

# endregion


# region DeleteAsync Method.

@pytest.mark.asyncio
async def test_DeleteAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    # Arrange
    service, _, _ = service_with_mocks

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        await service.DeleteAsync(None, session="session")
    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnTrue_WhenRecordIsDeleted(service_with_mocks):
    # Arrange
    service, repo_mock, _ = service_with_mocks