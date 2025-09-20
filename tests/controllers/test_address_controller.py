import pytest
import uuid
from unittest.mock import ANY

VALID_ADDRESS_ID = str(uuid.uuid4())
ANOTHER_ADDRESS_ID = str(uuid.uuid4())
NON_EXISTENT_ADDRESS_ID = str(uuid.uuid4())

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
    created = {**dto, "id": VALID_ADDRESS_ID}
    mock_service.CreateAsync.return_value = created

    # Act
    response = await client.post("/api/addresses/", json=dto)

    # Assert
    assert response.status_code == 201
    assert response.json() == created
    mock_service.CreateAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion

# region GetAll Method

@pytest.mark.asyncio
async def test_GetAll_ShouldReturn200_WithRecordList(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    entities = [
        {
            "id": VALID_ADDRESS_ID,
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "USA"
        },
        {
            "id": ANOTHER_ADDRESS_ID,
            "street": "456 Elm St",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02118",
            "country": "USA"
        }
    ]
    mock_service.GetAllAsync.return_value = entities

    # Act
    response = await client.get("/api/addresses/")

    # Assert
    assert response.status_code == 200
    assert response.json() == entities
    mock_service.GetAllAsync.assert_awaited_once_with(session=ANY)


@pytest.mark.asyncio
async def test_GetAll_ShouldReturn200_WithEmptyList(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.GetAllAsync.return_value = []

    # Act
    response = await client.get("/api/addresses/")

    # Assert
    assert response.status_code == 200
    assert response.json() == []
    mock_service.GetAllAsync.assert_awaited_once_with(session=ANY)

# endregion

# region GetById Method

@pytest.mark.asyncio
async def test_GetById_ShouldReturn200_WhenRecordExists(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    entity = {
        "id": VALID_ADDRESS_ID,
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    mock_service.GetByIdAsync.return_value = entity

    # Act
    response = await client.get(f"/api/addresses/{VALID_ADDRESS_ID}")

    # Assert
    assert response.status_code == 200
    assert response.json() == entity
    mock_service.GetByIdAsync.assert_awaited_once_with(ANY, session=ANY)


@pytest.mark.asyncio
async def test_GetById_ShouldReturn404_WhenRecordDoesNotExist(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.GetByIdAsync.return_value = None

    # Act
    response = await client.get(f"/api/addresses/{NON_EXISTENT_ADDRESS_ID}")

    # Assert
    assert response.status_code == 404
    mock_service.GetByIdAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion

# region Update Method

@pytest.mark.asyncio
async def test_Update_ShouldReturn200_WhenUpdateSucceeds(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    dto = {
        "id": VALID_ADDRESS_ID,
        "street": "Updated St",
        "city": "NYC",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    mock_service.UpdateAsync.return_value = True

    # Act
    response = await client.put("/api/addresses/", json=dto)

    # Assert
    assert response.status_code == 200
    mock_service.UpdateAsync.assert_awaited_once_with(ANY, session=ANY)


@pytest.mark.asyncio
async def test_Update_ShouldReturn404_WhenUpdateFails(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    dto = {
        "id": NON_EXISTENT_ADDRESS_ID,
        "street": "Updated St",
        "city": "NYC",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
    }
    mock_service.UpdateAsync.return_value = False

    # Act
    response = await client.put("/api/addresses/", json=dto)

    # Assert
    assert response.status_code == 404
    mock_service.UpdateAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion

# region Delete Method

@pytest.mark.asyncio
async def test_Delete_ShouldReturn204_WhenRecordIsDeleted(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.DeleteAsync.return_value = True

    # Act
    response = await client.delete(f"/api/addresses/{VALID_ADDRESS_ID}")

    # Assert
    assert response.status_code == 204
    mock_service.DeleteAsync.assert_awaited_once_with(ANY, session=ANY)


@pytest.mark.asyncio
async def test_Delete_ShouldReturn404_WhenRecordDoesNotExist(client_with_mocked_address_service):
    # Arrange
    client, mock_service = client_with_mocked_address_service
    mock_service.DeleteAsync.return_value = False

    # Act
    response = await client.delete(f"/api/addresses/{NON_EXISTENT_ADDRESS_ID}")

    # Assert
    assert response.status_code == 404
    mock_service.DeleteAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion
