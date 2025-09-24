import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from controllers import address_blp
from models.dtos.order.order_create_dto import OrderCreateDTO
from models.dtos.order.order_read_dto import OrderReadDTO
from models.dtos.order.order_update_dto import OrderUpdateDTO
from models.dtos.order.order_patch_dto import OrderPatchDTO
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

    def __init__(
        self,
        repository: OrderRepositoryInterface,
        address_repository: AddressRepositoryInterface,
        product_client: ProductServiceClient,
        logistics_client: LogisticsServiceClient
    ):
        self._repository = repository
        self._address_repository = address_repository
        self._product_client = product_client
        self._logistics_client = logistics_client


    async def CreateAsync(self, dto: OrderCreateDTO, session) -> OrderReadDTO:
        if dto is None:
            raise ValueError("Record data cannot be null.")

        if isinstance(dto, dict):
            dto = OrderCreateDTO(**dto)

        for item in dto.items:
            if item.product_variant_id:
                product_data = await self._product_client.get_variant(item.product_variant_id)

                if not product_data:
                    raise RuntimeError(f"Product Variant {item.product_variant_id} not found.")

                item.unit_price = Decimal(product_data["price"])
                await self._product_client.reserve_variant_stock(item.product_variant_id, item.quantity)

            else:
                product_data = await self._product_client.get_product(item.product_id)

                if not product_data:
                    raise RuntimeError(f"Product {item.product_id} not found.")

                item.unit_price = Decimal(product_data["price"])
                await self._product_client.reserve_product_stock(item.product_id, item.quantity)

        entity = Order(
            id=uuid.uuid4(),
            customer_id=dto.customer_id,
            created_at=datetime.now(timezone.utc),
            status=OrderStatus.PENDING,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    product_variant_id=item.product_variant_id,
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
                    product_variant_id=i.product_variant_id,
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
                        product_variant_id=i.product_variant_id,
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
                    product_variant_id=item.product_variant_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.unit_price * item.quantity
                )
                for item in entity.items
            ]
        )

    async def UpdateAsync(self, id: str, dto: OrderUpdateDTO, session) -> bool:
        if isinstance(dto, dict):
            dto = OrderUpdateDTO(**dto)

        if dto is None:
            raise ValueError("Record data cannot be null or missing an identifier.")

        existing = await self._repository.GetByIdAsync(id, session=session)
        if existing is None:
            return False

        if existing.status in [OrderStatus.PROCESSING, OrderStatus.IN_TRANSIT]:
            raise ValueError("Record can no longer be updated once processing or in transit.")

        existing.customer_id = dto.customer_id
        existing.status = dto.status
        existing.items = dto.items
        existing.shipment_id = dto.shipment_id
        existing.total_amount = dto.total_amount

        existing.updated_at = datetime.now(timezone.utc)

        await self._repository.UpdateAsync(existing, session=session)
        return True


    async def DeleteAsync(self, id: UUID, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")

        return await self._repository.DeleteAsync(id, session=session)


    async def PatchAsync(self, dto: OrderPatchDTO, session) -> bool:
        if isinstance(dto, dict):
            dto = OrderUpdateDTO(**dto)

        if dto is None or not dto.id:
            raise ValueError("Record data cannot be null or missing an identifier.")

        existing = await self._repository.GetByIdAsync(dto.id, session=session)
        if existing is None:
            return False

        if dto.status is not None:
            allowed_transitions = {
                OrderStatus.PENDING: {OrderStatus.PROCESSING, OrderStatus.CANCELLED},
                OrderStatus.PROCESSING: {OrderStatus.IN_TRANSIT, OrderStatus.CANCELLED},
                OrderStatus.IN_TRANSIT: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
                OrderStatus.COMPLETED: set(),   
                OrderStatus.CANCELLED: set(),
            }

            current_status = existing.status
            new_status = dto.status

            if new_status not in allowed_transitions.get(current_status, set()):
                raise ValueError(
                    f"Inappropriate status transition: {current_status.value} to {new_status.value}"
                )

            if new_status == OrderStatus.CANCELLED:
                for item in existing.items:
                    if item.product_variant_id:
                        await self._product_client.release_variant_stock(item.product_variant_id, item.quantity)
                    else:
                        await self._product_client.release_product_stock(item.product_id, item.quantity)

                if existing.shipment_id:
                    shipment_update_payload = {
                        "shipment_id": existing.shipment_id,
                        "status": "Cancelled"
                    }
                    await self._logistics_client.update_shipment(**shipment_update_payload)

            elif new_status == OrderStatus.COMPLETED:
                for item in existing.items:
                    if item.product_variant_id:
                        await self._product_client.reduce_variant_stock(item.product_variant_id, item.quantity)
                    else:
                        await self._product_client.reduce_product_stock(item.product_id, item.quantity)

            elif new_status == OrderStatus.PROCESSING:
                address_entity = await self._address_repository.GetByCustomerIdAsync(
                    existing.customer_id, session=session
                )
                if not address_entity:
                    raise ValueError(f"No address found for customer {existing.customer_id}")

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
