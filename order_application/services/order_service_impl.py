import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from models.dtos.order import OrderCreateDTO
from models.dtos.order import OrderReadDTO
from models.dtos.order import OrderUpdateDTO
from models.dtos.order import OrderPatchDTO
from models.dtos.order_item import OrderItemReadDTO
from models.entities import Order
from models.entities import OrderItem
from models.enums import OrderStatus
from repositories import AddressRepositoryInterface
from repositories.interfaces import OrderRepositoryInterface
from services.interfaces import OrderServiceInterface
from clients import ProductServiceClient
from clients import LogisticsServiceClient


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
            id=str(uuid.uuid4()),
            customer_id=str(dto.customer_id),
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
            OrderReadDTO.from_orm(e) for e in entities
        ]





    async def GetByIdAsync(self, id: str, session) -> Optional[OrderReadDTO]:
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


    async def DeleteAsync(self, id: str, session) -> bool:
        if not id:
            raise ValueError("Record identifier cannot be empty.")
        return await self._repository.DeleteAsync(id, session=session)

    async def PatchAsync(self, id: str, dto: OrderPatchDTO, session) -> bool:
        if isinstance(dto, dict):
            dto = OrderPatchDTO(**dto)

        if dto is None or not id:
            raise ValueError("Record data cannot be null or missing an identifier.")

        existing = await self._repository.GetByIdAsync(id, session=session)
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

            elif new_status == OrderStatus.IN_TRANSIT:
                if not existing.shipment_id:
                    raise ValueError("Cannot move to IN_TRANSIT: shipment does not exist.")

                shipment_status_response = await self._logistics_client.get_shipment(existing.shipment_id)
                if not shipment_status_response or shipment_status_response.get("status") != "InTransit":
                    raise ValueError("Shipment is not yet dispatched; cannot move order to IN_TRANSIT.")

                existing.status = OrderStatus.IN_TRANSIT


            elif new_status == OrderStatus.PROCESSING:

                if not existing.shipment_id:
                    address_entity = await self._address_repository.GetByCustomerIdAsync(
                        existing.customer_id, session=session
                    )
                    if not address_entity:
                        raise ValueError(f"No address found for customer {existing.customer_id}")

                    availability_payload = {
                        "street": address_entity.street,
                        "city": address_entity.city,
                        "state": address_entity.state,
                        "postalCode": address_entity.postal_code,
                        "country": address_entity.country
                    }

                    availability_response = await self._logistics_client.check_availability(**availability_payload)
                    if not availability_response or not availability_response.get("valid", False):
                        raise ValueError("Destination is not serviceable for shipping.")

                    shipment_payload = {
                        "order_id": str(existing.id),
                        "status": "Pending",
                        "dispatchDate": None,
                        "carrier": "DefaultCarrier",
                        "serviceLevel": "Standard",
                        **availability_payload
                    }

                    shipment_response = await self._logistics_client.create_shipment(**shipment_payload)
                    if not shipment_response or not shipment_response.get("id"):
                        raise RuntimeError("Shipment creation failed, order not saved.")

                    existing.shipment_id = shipment_response["id"]

            existing.status = new_status

        existing.updated_at = datetime.now(timezone.utc)

        await self._repository.UpdateAsync(existing, session=session)
        return True
