import pytest
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from services.address_service_impl import AddressService
from models.entities.address import Address
from models.dtos.address.address_create_dto import AddressCreateDTO
from models.dtos.address.address_update_dto import AddressUpdateDTO


@pytest.fixture
def service_with_mocks():
    repo_mock = AsyncMock()
    service = AddressService(repo_mock)
    return service, repo_mock


# region CreateAsync Method.

@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseValueError_WhenDTOIsNone(service_with_mocks):
    service, repo_mock = service_with_mocks

    with pytest.raises(ValueError):
        await service.CreateAsync(None, session="session")

    repo_mock.AddAsync.assert_not_called()


@pytest.mark.asyncio
async def test_CreateAsync_ShouldReturnDTO_WhenDTOIsValid(service_with_mocks):
    service, repo_mock = service_with_mocks

    dto = AddressCreateDTO(
        customer_id=str(uuid.uuid4),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )

    result = await service.CreateAsync(dto, session="session")

    assert isinstance(result.id, str)
    assert result.street == dto.street
    assert result.city == dto.city
    assert result.state == dto.state
    assert result.postal_code == dto.postal_code
    assert result.country == dto.country
    repo_mock.AddAsync.assert_awaited_once()


@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock = service_with_mocks

    dto = AddressCreateDTO(
        customer_id=str(uuid.uuid4),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    repo_mock.AddAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception) as exc_info:
        await service.CreateAsync(dto, session="session")

    assert "Repository failure" in str(exc_info.value)
    repo_mock.AddAsync.assert_awaited_once()

# endregion


# region GetAllAsync Method.

@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnEmptyList_WhenNoRecordsExist(service_with_mocks):
    service, repo_mock = service_with_mocks

    repo_mock.GetAllAsync.return_value = None
    result = await service.GetAllAsync(session="session")

    assert result == []
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnMappedDTOs_WhenRecordsExist(service_with_mocks):
    service, repo_mock = service_with_mocks

    addr1 = Address(
        id=str(uuid.uuid4),
        street="123 Main St",
        customer_id=str(uuid.uuid4),
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA",
        created_at=datetime.now(timezone.utc)
    )
    addr2 = Address(
        id=str(uuid.uuid4),
        customer_id=str(uuid.uuid4),
        street="456 Elm St",
        city="Boston",
        state="MA",
        postal_code="02118",
        country="USA",
        created_at=datetime.now(timezone.utc)
    )
    repo_mock.GetAllAsync.return_value = [addr1, addr2]

    result = await service.GetAllAsync(session="session")

    assert len(result) == 2
    assert result[0].street == "123 Main St"
    assert result[1].city == "Boston"
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock = service_with_mocks

    repo_mock.GetAllAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.GetAllAsync(session="session")

# endregion


# region GetByIdAsync Method.

@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    service, _ = service_with_mocks

    with pytest.raises(ValueError):
        await service.GetByIdAsync(None, session="session")


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnMappedDTO_WhenRecordExists(service_with_mocks):
    service, repo_mock = service_with_mocks

    address_id = str(uuid.uuid4)
    entity = Address(
        id=address_id,
        customer_id=str(uuid.uuid4),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA",
        created_at=datetime.now(timezone.utc)
    )
    repo_mock.GetByIdAsync.return_value = entity

    result = await service.GetByIdAsync(address_id, session="session")

    assert result.id == address_id
    assert result.street == "123 Main St"
    repo_mock.GetByIdAsync.assert_awaited_once_with(address_id, session="session")


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnNone_WhenRecordDoesNotExist(service_with_mocks):
    service, repo_mock = service_with_mocks

    address_id = str(uuid.uuid4)
    repo_mock.GetByIdAsync.return_value = None

    result = await service.GetByIdAsync(address_id, session="session")

    assert result is None
    repo_mock.GetByIdAsync.assert_awaited_once_with(address_id, session="session")


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock = service_with_mocks

    repo_mock.GetByIdAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.GetByIdAsync(str(uuid.uuid4), session="session")

# endregion


# region UpdateAsync Method.

@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseValueError_WhenDTOisNullOrIdIsEmpty(service_with_mocks):
    service, _ = service_with_mocks

    with pytest.raises(ValueError):
        await service.UpdateAsync(None, session="session")

    with pytest.raises(ValueError):
        await service.UpdateAsync(AddressUpdateDTO(id=None), session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnFalse_WhenRecordDoesNotExist(service_with_mocks):
    service, repo_mock = service_with_mocks

    dto = AddressUpdateDTO(
        id=str(uuid.uuid4),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    repo_mock.GetByIdAsync.return_value = None

    result = await service.UpdateAsync(dto, session="session")

    assert result is False
    repo_mock.GetByIdAsync.assert_awaited_once_with(dto.id, session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnTrue_WhenUpdateIsSuccessful(service_with_mocks):
    service, repo_mock = service_with_mocks

    dto = AddressUpdateDTO(
        id=str(uuid.uuid4),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    existing = Address()
    repo_mock.GetByIdAsync.return_value = existing

    result = await service.UpdateAsync(dto, session="session")

    assert result is True
    assert existing.street == "123 Main St"
    assert existing.city == "NY"
    repo_mock.UpdateAsync.assert_awaited_once_with(existing, session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock = service_with_mocks

    dto = AddressUpdateDTO(
        id=str(uuid.uuid4),
        street="123 Main St",
        city="NY",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    repo_mock.GetByIdAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.UpdateAsync(dto, session="session")

# endregion


# region DeleteAsync Method.

@pytest.mark.asyncio
async def test_DeleteAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    service, _ = service_with_mocks

    with pytest.raises(ValueError):
        await service.DeleteAsync(None, session="session")


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnTrue_WhenRecordIsDeleted(service_with_mocks):
    service, repo_mock = service_with_mocks

    address_id = str(uuid.uuid4)
    repo_mock.DeleteAsync.return_value = True

    result = await service.DeleteAsync(address_id, session="session")

    assert result is True
    repo_mock.DeleteAsync.assert_awaited_once_with(address_id, session="session")


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnFalse_WhenRecordDoesNotExist(service_with_mocks):
    service, repo_mock = service_with_mocks

    address_id = str(uuid.uuid4)
    repo_mock.DeleteAsync.return_value = False

    result = await service.DeleteAsync(address_id, session="session")

    assert result is False
    repo_mock.DeleteAsync.assert_awaited_once_with(address_id, session="session")


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock = service_with_mocks

    repo_mock.DeleteAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.DeleteAsync(str(uuid.uuid4), session="session")

# endregion