import pytest
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock

from services.order_service_impl import OrderService
from models.entities.order import Order
from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO
from models.enums.order_status import OrderStatus


@pytest.fixture
def service_with_mocks():
    repo_mock = AsyncMock()
    address_repo_mock = AsyncMock()
    product_client_mock = AsyncMock()
    logistics_client_mock = AsyncMock()
    service = OrderService(
        repo_mock,
        address_repo_mock,
        product_client_mock,
        logistics_client_mock
    )
    return service, repo_mock, address_repo_mock, product_client_mock, logistics_client_mock


# region CreateAsync Method.

@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseValueError_WhenDTOIsNone(service_with_mocks):
    service, repo_mock, _, product_client_mock, logistics_client_mock = service_with_mocks

    with pytest.raises(ValueError):
        await service.CreateAsync(None, session="session")

    repo_mock.AddAsync.assert_not_called()
    product_client_mock.get_product.assert_not_called()
    product_client_mock.get_variant.assert_not_called()
    logistics_client_mock.create_shipment.assert_not_called()


@pytest.mark.asyncio
async def test_CreateAsync_ShouldReturnDTO_WhenDTOIsValid(service_with_mocks):
    service, repo_mock, _, product_client_mock, _ = service_with_mocks

    dto = OrderCreateDTO(customer_id=str4(), items=[])
    repo_mock.AddAsync.return_value = None

    result = await service.CreateAsync(dto, session="session")

    assert isinstance(result.id, str)
    assert result.customer_id == dto.customer_id
    assert result.status == OrderStatus.PENDING
    assert result.total_amount == 0
    repo_mock.AddAsync.assert_awaited_once()


@pytest.mark.asyncio
async def test_CreateAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    dto = OrderCreateDTO(customer_id=str4(), items=[])
    repo_mock.AddAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception) as exc_info:
        await service.CreateAsync(dto, session="session")

    assert "Repository failure" in str(exc_info.value)
    repo_mock.AddAsync.assert_awaited_once()

# endregion


# region GetAllAsync Method.

@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnEmptyList_WhenNoRecordsExist(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    repo_mock.GetAllAsync.return_value = None
    result = await service.GetAllAsync(session="session")

    assert result == []
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnMappedDTOs_WhenRecordsExist(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    order = Order(
        id=str4(),
        customer_id=str4(),
        created_at=datetime.now(timezone.utc),
        total_amount=Decimal("10.00"),
        status=OrderStatus.PENDING,
        items=[]
    )
    repo_mock.GetAllAsync.return_value = [order]

    result = await service.GetAllAsync(session="session")

    assert len(result) == 1
    assert result[0].id == order.id
    repo_mock.GetAllAsync.assert_awaited_once_with(session="session")


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    repo_mock.GetAllAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.GetAllAsync(session="session")

# endregion


# region GetByIdAsync Method.

@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseValueError_WhenIdIsEmpty(service_with_mocks):
    service, _, _, _, _ = service_with_mocks

    with pytest.raises(ValueError):
        await service.GetByIdAsync(None, session="session")


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnMappedDTO_WhenRecordExists(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    order_id = str4()
    order = Order(
        id=order_id,
        customer_id=str4(),
        created_at=datetime.now(timezone.utc),
        total_amount=Decimal("20.00"),
        status=OrderStatus.PENDING,
        items=[]
    )
    repo_mock.GetByIdAsync.return_value = order

    result = await service.GetByIdAsync(order_id, session="session")

    assert result.id == order_id
    repo_mock.GetByIdAsync.assert_awaited_once_with(order_id, session="session")


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    repo_mock.GetByIdAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.GetByIdAsync(str4(), session="session")

# endregion


# region UpdateAsync Method.

@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseValueError_WhenDTOisNullOrIdIsEmpty(service_with_mocks):
    service, _, _, _, _ = service_with_mocks

    with pytest.raises(ValueError):
        await service.UpdateAsync(None, session="session")

    with pytest.raises(ValueError):
        await service.UpdateAsync(OrderUpdateDTO(id=None), session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnTrue_WhenUpdateIsSuccessful(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    dto = OrderUpdateDTO(id=str4(), status=OrderStatus.PENDING)
    existing_order = Order(id=dto.id, items=[])
    repo_mock.GetByIdAsync.return_value = existing_order

    result = await service.UpdateAsync(dto, session="session")

    assert result is True
    repo_mock.UpdateAsync.assert_awaited_once_with(existing_order, session="session")


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    dto = OrderUpdateDTO(id=str4(), status=OrderStatus.PENDING)
    repo_mock.GetByIdAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.UpdateAsync(dto, session="session")

# endregion


# region DeleteAsync Method.

@pytest.mark.asyncio
async def test_DeleteAsync_ShouldCallRepository_WithCorrectId(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    order_id = str4()
    repo_mock.DeleteAsync.return_value = True

    result = await service.DeleteAsync(order_id, session="session")

    assert result is True
    repo_mock.DeleteAsync.assert_awaited_once_with(order_id, session="session")


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldRaiseException_WhenRepositoryFails(service_with_mocks):
    service, repo_mock, _, _, _ = service_with_mocks

    repo_mock.DeleteAsync.side_effect = Exception("Repository failure")

    with pytest.raises(Exception):
        await service.DeleteAsync(str4(), session="session")

# endregion
