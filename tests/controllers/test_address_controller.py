import pytest

# region Create Method

@pytest.mark.asyncio
async def test_Create_ShouldReturn201_WhenRecordIsCreated(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    dto = {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    created = {**dto, "id": "abc123"}
    mock_service.CreateAsync.return_value = created

    # Act
    act = await client.post("/api/addresses/", json=dto)

    # Assert
    assert act.status_code == 201
    assert act.json() == created
    mock_service.CreateAsync.assert_awaited_once_with(dto)

# endregion

# region GetAll Method

@pytest.mark.asyncio
async def test_GetAll_ShouldReturn200_WithRecordList(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    entities = [
        {"id": "1", "street": "123 Main St"},
        {"id": "2", "street": "456 Elm St"}
    ]
    mock_service.GetAllAsync.return_value = entities

    # Act
    act = await client.get("/api/addresses/")

    # Assert
    assert act.status_code == 200
    assert act.json() == entities
    mock_service.GetAllAsync.assert_awaited_once()

# endregion

# region GetById Method

@pytest.mark.asyncio
async def test_GetById_ShouldReturn200_WhenRecordExists(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    entity = {"id": "1", "street": "123 Main St"}
    mock_service.GetByIdAsync.return_value = entity

    # Act
    act = await client.get("/api/addresses/1")

    # Assert
    assert act.status_code == 200
    assert act.json() == entity
    mock_service.GetByIdAsync.assert_awaited_once_with("1")

@pytest.mark.asyncio
async def test_GetById_ShouldReturn404_WhenRecordDoesNotExist(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.GetByIdAsync.return_value = None

    # Act
    act = await client.get("/api/addresses/999")

    # Assert
    assert act.status_code == 404
    mock_service.GetByIdAsync.assert_awaited_once_with("999")

# endregion

# region Update Method

@pytest.mark.asyncio
async def test_Update_ShouldReturn200_WhenUpdateSucceeds(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    dto = {
        "id": "1",
        "street": "Updated St",
        "city": "NYC",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    mock_service.UpdateAsync.return_value = True

    # Act
    act = await client.put("/api/addresses/", json=dto)

    # Assert
    assert act.status_code == 200
    mock_service.UpdateAsync.assert_awaited_once_with(dto)

@pytest.mark.asyncio
async def test_Update_ShouldReturn404_WhenUpdateFails(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    dto = {
        "id": "1",
        "street": "Updated St",
        "city": "NYC",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    mock_service.UpdateAsync.return_value = False

    # Act
    act = await client.put("/api/addresses/", json=dto)

    # Assert
    assert act.status_code == 404
    mock_service.UpdateAsync.assert_awaited_once_with(dto)

# endregion

# region Delete Method

@pytest.mark.asyncio
async def test_Delete_ShouldReturn204_WhenRecordIsDeleted(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.DeleteAsync.return_value = True

    # Act
    act = await client.delete("/api/addresses/1")

    # Assert
    assert act.status_code == 204
    mock_service.DeleteAsync.assert_awaited_once_with("1")

@pytest.mark.asyncio
async def test_Delete_ShouldReturn404_WhenRecordDoesNotExist(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.DeleteAsync.return_value = False

    # Act
    act = await client.delete("/api/addresses/999")

    # Assert
    assert act.status_code == 404
    mock_service.DeleteAsync.assert_awaited_once_with("999")

# endregion
