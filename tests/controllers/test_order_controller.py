import pytest
import uuid
from datetime import datetime, timezone
from unittest.mock import ANY
from copy import deepcopy
from decimal import Decimal

VALID_ORDER_ID = str(uuid.uuid4())
VALID_CUSTOMER_ID = str(uuid.uuid4())
VALID_PRODUCT_ID = str(uuid.uuid4())


def full_order_dict(order_id=None, customer_id=None, status="PENDING"):
    return {
        "id": uuid.UUID(order_id) if order_id else uuid.uuid4(),
        "created_at": datetime.now(timezone.utc),
        "updated_at": None,
        "customer_id": uuid.UUID(customer_id) if customer_id else uuid.uuid4(),
        "total_amount": Decimal("100.00"),
        "status": status,
        "items": [
            {
                "product_id": uuid.UUID(VALID_PRODUCT_ID),
                "quantity": 2,
                "unit_price": 50.00
            }
        ]
    }


def normalise_order_for_json(order):
    order_json = deepcopy(order)
    order_json["id"] = str(order_json["id"])
    order_json["customer_id"] = str(order_json["customer_id"])
    order_json["created_at"] = order_json["created_at"].isoformat()
    order_json["total_amount"] = str(order_json["total_amount"])
    for item in order_json["items"]:
        item["product_id"] = str(item["product_id"])
        item["total_price"] = round(item["unit_price"] * item["quantity"], 2)
    return order_json


# region Create Method.

@pytest.mark.asyncio
async def test_Create_ShouldReturnCreatedAtAction_WhenRecordIsCreated(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    dto = {
        "customer_id": VALID_CUSTOMER_ID,
        "items": [{"product_id": VALID_PRODUCT_ID, "quantity": 2, "unit_price": 50.00}]
    }
    expected = full_order_dict(order_id=VALID_ORDER_ID, customer_id=VALID_CUSTOMER_ID)
    mock_service.CreateAsync.return_value = expected

    # Act
    response = await client.post("/api/orders/", json=dto)

    # Assert
    assert response.status_code == 201
    assert response.json() == normalise_order_for_json(expected)
    mock_service.CreateAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion


# region GetAll Method.

@pytest.mark.asyncio
async def test_GetAll_ShouldReturnOk_WithRecordList(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    orders = [
        full_order_dict(order_id=VALID_ORDER_ID, customer_id=VALID_CUSTOMER_ID, status="PENDING"),
        full_order_dict(status="Shipped")
    ]
    mock_service.GetAllAsync.return_value = orders

    # Act
    response = await client.get("/api/orders/")

    # Assert
    assert response.status_code == 200
    assert response.json() == [normalise_order_for_json(o) for o in orders]
    mock_service.GetAllAsync.assert_awaited_once_with(session=ANY)

# endregion


# region GetById Method.

@pytest.mark.asyncio
async def test_GetById_ShouldReturnOk_WhenRecordExists(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    order = full_order_dict(order_id=VALID_ORDER_ID, customer_id=VALID_CUSTOMER_ID)
    mock_service.GetByIdAsync.return_value = order

    # Act
    response = await client.get(f"/api/orders/{VALID_ORDER_ID}")

    # Assert
    assert response.status_code == 200
    assert response.json() == normalise_order_for_json(order)
    mock_service.GetByIdAsync.assert_awaited_once_with(ANY, session=ANY)


@pytest.mark.asyncio
async def test_GetById_ShouldReturnNotFound_WhenRecordDoesNotExist(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    mock_service.GetByIdAsync.return_value = None
    random_id = str(uuid.uuid4())

    # Act
    response = await client.get(f"/api/orders/{random_id}")

    # Assert
    assert response.status_code == 404
    mock_service.GetByIdAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion


# region Update Method.

@pytest.mark.asyncio
async def test_Update_ShouldReturnOk_WhenUpdateSucceeds(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    dto = {"id": VALID_ORDER_ID, "status": "Shipped"}
    mock_service.UpdateAsync.return_value = True

    # Act
    response = await client.put("/api/orders/", json=dto)

    # Assert
    assert response.status_code == 200
    mock_service.UpdateAsync.assert_awaited_once_with(ANY, session=ANY)


@pytest.mark.asyncio
async def test_Update_ShouldReturnNotFound_WhenUpdateFails(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    dto = {"id": VALID_ORDER_ID, "status": "Shipped"}
    mock_service.UpdateAsync.return_value = False

    # Act
    response = await client.put("/api/orders/", json=dto)

    # Assert
    assert response.status_code == 404
    mock_service.UpdateAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion


# region Delete Method.

@pytest.mark.asyncio
async def test_Delete_ShouldReturnNoContent_WhenRecordIsDeleted(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    mock_service.DeleteAsync.return_value = True

    # Act
    response = await client.delete(f"/api/orders/{VALID_ORDER_ID}")

    # Assert
    assert response.status_code == 204
    mock_service.DeleteAsync.assert_awaited_once_with(ANY, session=ANY)


@pytest.mark.asyncio
async def test_Delete_ShouldReturnNotFound_WhenRecordDoesNotExist(client_with_mocked_order_service):
    # Arrange
    client, mock_service = client_with_mocked_order_service
    mock_service.DeleteAsync.return_value = False
    random_id = str(uuid.uuid4())

    # Act
    response = await client.delete(f"/api/orders/{random_id}")

    # Assert
    assert response.status_code == 404
    mock_service.DeleteAsync.assert_awaited_once_with(ANY, session=ANY)

# endregion
