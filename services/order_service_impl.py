import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from controllers import address_blp
from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_read_dto import OrderReadDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO
from models.dtos.order_item.order_item_read_dto import OrderItemReadDTO
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.enums.order_status import OrderStatus
from repositories.address_repository_impl import AddressRepositoryInterface
from repositories.interfaces.order_repository_interface import OrderRepositoryInterface
from services.interfaces.order_service_interface import OrderServiceInterface
from clients.product_service_client import ProductServiceClient
from clients.logistics_service_client import LogisticsServiceClient

class OrderService(OrderServiceInterface):

    def __init__(self, repository: OrderRepositoryInterface, address_repository: AddressRepositoryInterface, product_client: ProductServiceClient, logistics_client: LogisticsServiceClient):
        self._repository = repository
        self._address_repository = address_repository
        self._product_client = product_client
        self._logistics_client = logistics_client

    async def CreateAsync(self, dto: OrderCreateDTO, session) -> OrderReadDTO:
        if dto is None:
            raise ValueError("Record data cannot be null.")
        if isinstance(dto, dict):
            dto = OrderCreateDTO(**dto)

        # Get product prices from external API
        for item in dto.items:
            product_data = await self._product_client.get_product(item.product_id)
            if not product_data:
                raise RuntimeError(f"Product {item.product_id} not found.")
            item.unit_price = Decimal(product_data["price"])

        # Prepare order entity (not yet saved)
        entity = Order(
            id=uuid.uuid4(),
            customer_id=dto.customer_id,
            created_at=datetime.now(timezone.utc),
            status=OrderStatus.PENDING,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price
                )
                for item in dto.items
            ]
        )
        entity.total_amount = sum(
            Decimal(item.unit_price) * item.quantity for item in entity.items
        )

        await self._repository.AddAsync(entity, session=session)

        return OrderReadDTO(
            id=entity.id,
            created_at=entity.created_at,
            customer_id=entity.customer_id,
            shipment_id=entity.shipment_id,
            total_amount=entity.total_amount,
            status=entity.status,
            items=[
                OrderItemReadDTO(
                    id=i.id,
                    product_id=i.product_id,
                    quantity=i.quantity,
                    unit_price=i.unit_price,
                    total_price=i.unit_price * i.quantity
                )
                for i in entity.items
            ]
        )

    async def GetAllAsync(self, session) -> List[OrderReadDTO]:
        entities = await self._repository.GetAllAsync(session=session)
        if not entities:
            return []
        return [
            OrderReadDTO(
                id=e.id,
                created_at=e.created_at,
                customer_id=e.customer_id,
                shipment_id=e.shipment_id,
                total_amount=e.total_amount,
                status=e.status,
                items=[
                    OrderItemReadDTO(
                        id=i.id,
                        product_id=i.product_id,
                        quantity=i.quantity,
                        unit_price=i.unit_price,
                        total_price=i.unit_price * i.quantity
                    )
                    for i in e.items
                ]
            )
            for e in entities
        ]

    async def GetByIdAsync(self, id: UUID, session) -> Optional[OrderReadDTO]:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        entity = await self._repository.GetByIdAsync(id, session=session)
        if entity is None:
            return None

        return OrderReadDTO(
            id=entity.id,
            created_at=entity.created_at,
            customer_id=entity.customer_id,
            shipment_id=entity.shipment_id,
            total_amount=entity.total_amount,
            status=entity.status,
            items=[
                OrderItemReadDTO(
                    id=item.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.unit_price * item.quantity
                )
                for item in entity.items
            ]
        )

    async def UpdateAsync(self, dto: OrderUpdateDTO, session) -> bool:
        if isinstance(dto, dict):
            dto = OrderUpdateDTO(**dto)

        if dto is None or not dto.id:
            raise ValueError("Record data cannot be null or missing an identifier.")

        existing = await self._repository.GetByIdAsync(dto.id, session=session)
        if existing is None:
            return False

        if dto.status is not None:
            existing.status = dto.status

            # Shipment creation trigger
            if dto.status == OrderStatus.PROCESSING:
                # Check address from DB
                address_entity = await self._address_repository.GetByCustomerIdAsync(
                    existing.customer_id, session=session
                )
                if not address_entity:
                    raise ValueError(f"No address found for customer {existing.customer_id}")

                # Call shipment API BEFORE saving
                shipment_payload = {
                    "order_id": str(existing.id),
                    "status": "Pending",
                    "dispatchDate": None,
                    "carrier": "DefaultCarrier",
                    "serviceLevel": "Standard",
                    "street": address_entity.street,
                    "city": address_entity.city,
                    "state": address_entity.state,
                    "postalCode": address_entity.postal_code,
                    "country": address_entity.country
                }

                shipment_response = await self._logistics_client.create_shipment(**shipment_payload)
                if not shipment_response or not shipment_response.get("id"):
                    raise RuntimeError("Shipment creation failed, order not saved.")

                existing.shipment_id = shipment_response["id"]

        existing.updated_at = datetime.now(timezone.utc)
        await self._repository.UpdateAsync(existing, session=session)
        return True


    async def DeleteAsync(self, id: UUID, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")
        return await self._repository.DeleteAsync(id, session=session)
