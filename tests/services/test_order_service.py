import pytest
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from services.order_service_impl import OrderService
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO
from models.enums.order_status import OrderStatus


@pytest.fixture
def service_with_mocks():
    repo_mock = AsyncMock()
    mapper_mock = MagicMock()
    service = OrderService(repo_mock, mapper_mock)
    return service, repo_mock, mapper_mock


# region CreateAsync Method.

@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseValueError_WhenDTOIsNone(service_with_mocks):
    service, repo_mock, mapper_mock = service_with_mocks

    with pytest.raises(ValueError) as exc_info:
        await service.CreateAsync(None, session="session")
    assert "cannot be null" in str(exc_info.value)
    repo_mock.AddAsync.assert_not_called()


@pytest.mark.asyncio
async def test_CreateAsync_ShouldReturnDTO_WhenDTOIsValid(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    create_dto = OrderCreateDTO(customer_id=uuid.uuid4(), items=[])
    # Simulate repository AddAsync doing nothing special
    repo_mock.AddAsync.return_value = None

    result = await service.CreateAsync(create_dto, session="session")

    assert isinstance(result.id, uuid.UUID)
    assert result.customer_id == create_dto.customer_id
    assert result.status == OrderStatus.PENDING.value
    assert result.total_amount == 0
    repo_mock.AddAsync.assert_awaited_once()
    

@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    create_dto = OrderCreateDTO(customer_id=uuid.uuid4(), items=[])
    repo_mock.AddAsync.side_effect = Exception("Repository failure.")

    with pytest.raises(Exception) as exc_info:
        await service.CreateAsync(create_dto, session="session")
    assert "Repository failure." in str(exc_info.value)
    repo_mock.AddAsync.assert_awaited_once()

# endregion


# region GetAllAsync Method.

@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnList_WhenRecordsExist(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    order1 = Order(
        id=uuid.uuid4(),
        customer_id=uuid.uuid4(),
        created_at=datetime.now(timezone.utc),
        total_amount=Decimal("50.00"),
        status=OrderStatus.PENDING,
        items=[]
    )
    order2 = Order(
        id=uuid.uuid4(),
        customer_id=uuid.uuid4(),
        created_at=datetime.now(timezone.utc),
        total_amount=Decimal("75.00"),
        status=OrderStatus.SHIPPED,
        items=[]
    )
    repo_mock.GetAllAsync.return_value = [order1, order2]

    result = await service.GetAllAsync(session="session")

    assert len(result) == 2
    assert result[0].id == order1.id
    assert result[1].status == order2.status.value
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnEmptyList_WhenNoRecordsExist(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    repo_mock.GetAllAsync.return_value = None

    result = await service.GetAllAsync(session="session")

    assert result == []
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")

# endregion


# region GetByIdAsync Method.

@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    service, _, _ = service_with_mocks

    with pytest.raises(ValueError) as exc_info:
        await service.GetByIdAsync(None, session="session")
    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnDTO_WhenRecordExists(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    order_id = uuid.uuid4()
    entity = Order(
        id=order_id,
        customer_id=uuid.uuid4(),
        created_at=datetime.now(timezone.utc),
        total_amount=Decimal("100.00"),
        status=OrderStatus.PENDING,
        items=[]
    )
    repo_mock.GetByIdAsync.return_value = entity

    result = await service.GetByIdAsync(order_id, session="session")

    assert result.id == order_id
    assert result.status == OrderStatus.PENDING.value
    repo_mock.GetByIdAsync.assert_awaited_once_with(order_id, session="session")


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnNone_WhenRecordDoesNotExist(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    order_id = uuid.uuid4()
    repo_mock.GetByIdAsync.return_value = None

    result = await service.GetByIdAsync(order_id, session="session")

    assert result is None
    repo_mock.GetByIdAsync.assert_awaited_once_with(order_id, session="session")

# endregion


# region UpdateAsync Method.

@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseValueError_WhenDTOIsInvalid(service_with_mocks):
    service, _, _ = service_with_mocks

    with pytest.raises(ValueError) as exc_info:
        await service.UpdateAsync(None, session="session")
    assert "cannot be null" in str(exc_info.value)


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnFalse_WhenRecordDoesNotExist(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    dto = OrderUpdateDTO(id=uuid.uuid4(), items=[])
    repo_mock.GetByIdAsync.return_value = None

    result = await service.UpdateAsync(dto, session="session")

    assert result is False
    repo_mock.GetByIdAsync.assert_awaited_once_with(dto.id, session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnTrue_WhenUpdateSucceeds(service_with_mocks):
    service, repo_mock, mapper_mock = service_with_mocks
    dto = OrderUpdateDTO(id=uuid.uuid4(), customer_id=uuid.uuid4(), items=[])
    existing = Order()
    repo_mock.GetByIdAsync.return_value = existing

    result = await service.UpdateAsync(dto, session="session")

    assert result is True
    assert existing.customer_id == dto.customer_id
    repo_mock.UpdateAsync.assert_awaited_once_with(existing, session="session")


# endregion


# region DeleteAsync Method.

@pytest.mark.asyncio
async def test_DeleteAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    service, _, _ = service_with_mocks

    with pytest.raises(ValueError) as exc_info:
        await service.DeleteAsync(None, session="session")
    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnTrue_WhenRecordIsDeleted(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    order_id = uuid.uuid4()
    repo_mock.DeleteAsync.return_value = True

    result = await service.DeleteAsync(order_id, session="session")

    assert result is True
    repo_mock.DeleteAsync.assert_awaited_once_with(order_id, session="session")


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnFalse_WhenRecordDoesNotExist(service_with_mocks):
    service, repo_mock, _ = service_with_mocks
    order_id = uuid.uuid4()
    repo_mock.DeleteAsync.return_value = False

    result = await service.DeleteAsync(order_id, session="session")

    assert result is False
    repo_mock.DeleteAsync.assert_awaited_once_with(order_id, session="session")

# endregion
