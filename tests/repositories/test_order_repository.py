import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from repositories.order_repository_impl import OrderRepository
from models.entities.order import Order


@pytest.fixture
def repo_with_mocks():
    session_factory = MagicMock()  # Not used directly in these tests
    return OrderRepository(session_factory)


# region AddAsync Method.

@pytest.mark.asyncio
async def test_AddAsync_ShouldRaiseValueError_WhenEntityIsNone(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()

    with pytest.raises(ValueError) as exc_info:
        await repo.AddAsync(None, session=session_mock)
    assert "cannot be null" in str(exc_info.value)
    session_mock.add.assert_not_called()


@pytest.mark.asyncio
async def test_AddAsync_ShouldAddEntity_WhenValid(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    entity = Order(id=uuid.uuid4())

    result = await repo.AddAsync(entity, session=session_mock)

    assert result == entity
    session_mock.add.assert_called_once_with(entity)
    session_mock.commit.assert_awaited_once()
    session_mock.refresh.assert_awaited_once_with(entity)

# endregion


# region GetAllAsync Method.

@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnList_WhenRecordsExist(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    orders = [Order(id=uuid.uuid4()), Order(id=uuid.uuid4())]
    execute_result = MagicMock()
    execute_result.scalars.return_value.all.return_value = orders
    session_mock.execute.return_value = execute_result

    result = await repo.GetAllAsync(session=session_mock)

    assert result == orders
    session_mock.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_GetAllAsync_ShouldReturnEmptyList_WhenNoRecords(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    execute_result = MagicMock()
    execute_result.scalars.return_value.all.return_value = []
    session_mock.execute.return_value = execute_result

    result = await repo.GetAllAsync(session=session_mock)

    assert result == []
    session_mock.execute.assert_awaited_once()

# endregion


# region GetByIdAsync Method.

@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldRaiseValueError_WhenIdIsEmpty(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()

    with pytest.raises(ValueError) as exc_info:
        await repo.GetByIdAsync(None, session=session_mock)
    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnEntity_WhenRecordExists(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    order_id = uuid.uuid4()
    order = Order(id=order_id)
    execute_result = MagicMock()
    execute_result.scalars.return_value.first.return_value = order
    session_mock.execute.return_value = execute_result

    result = await repo.GetByIdAsync(order_id, session=session_mock)

    assert result == order
    session_mock.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_GetByIdAsync_ShouldReturnNone_WhenRecordDoesNotExist(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    order_id = uuid.uuid4()
    execute_result = MagicMock()
    execute_result.scalars.return_value.first.return_value = None
    session_mock.execute.return_value = execute_result

    result = await repo.GetByIdAsync(order_id, session=session_mock)

    assert result is None
    session_mock.execute.assert_awaited_once()

# endregion


# region UpdateAsync Method.

@pytest.mark.asyncio
async def test_UpdateAsync_ShouldRaiseValueError_WhenEntityIsNone(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()

    with pytest.raises(ValueError) as exc_info:
        await repo.UpdateAsync(None, session=session_mock)
    assert "cannot be null" in str(exc_info.value)


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnFalse_WhenRecordDoesNotExist(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    updated = Order(id=uuid.uuid4())
    repo.GetByIdAsync = AsyncMock(return_value=None)

    result = await repo.UpdateAsync(updated, session=session_mock)

    assert result is False
    repo.GetByIdAsync.assert_awaited_once_with(updated.id, session=session_mock)


@pytest.mark.asyncio
async def test_UpdateAsync_ShouldReturnTrue_WhenUpdateSucceeds(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    updated = Order(id=uuid.uuid4())
    existing = Order(id=updated.id)
    repo.GetByIdAsync = AsyncMock(return_value=existing)

    result = await repo.UpdateAsync(updated, session=session_mock)

    assert result is True
    session_mock.commit.assert_awaited_once()

# endregion


# region DeleteAsync Method.

@pytest.mark.asyncio
async def test_DeleteAsync_ShouldRaiseValueError_WhenIdIsEmpty(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()

    with pytest.raises(ValueError) as exc_info:
        await repo.DeleteAsync(None, session=session_mock)
    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnFalse_WhenRecordDoesNotExist(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    order_id = uuid.uuid4()
    repo.GetByIdAsync = AsyncMock(return_value=None)

    result = await repo.DeleteAsync(order_id, session=session_mock)

    assert result is False
    repo.GetByIdAsync.assert_awaited_once_with(order_id, session=session_mock)


@pytest.mark.asyncio
async def test_DeleteAsync_ShouldReturnTrue_WhenDeleteSucceeds(repo_with_mocks):
    repo = repo_with_mocks
    session_mock = AsyncMock()
    order_id = uuid.uuid4()
    existing = Order(id=order_id)
    repo.GetByIdAsync = AsyncMock(return_value=existing)

    result = await repo.DeleteAsync(order_id, session=session_mock)

    assert result is True
    session_mock.delete.assert_awaited_once_with(existing)
    session_mock.commit.assert_awaited_once()

# endregion
