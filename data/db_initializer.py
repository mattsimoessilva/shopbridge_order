import asyncio
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.entities.base import Base
from models.entities.address import Address
from models.entities.order import Order
from models.entities.order_item import OrderItem
from models.enums.order_status import OrderStatus


async def initialize_database():
    engine = create_async_engine("sqlite+aiosqlite:///./order.db", echo=True, future=True)
    async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:

        # Step 1: Seed Addresses
        addresses = [
            Address(id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"), customer_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", street="742 Evergreen Terrace", city="Springfield", state="IL", postal_code="62704", country="USA"),
            Address(id=uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"), customer_id="44444444-4444-4444-4444-444444444444", street="221B Baker Street", city="London", state="LDN", postal_code="NW1 6XE", country="UK"),
            Address(id=uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"), customer_id="55555555-5555-5555-5555-555555555555", street="12 Grimmauld Place", city="London", state="LDN", postal_code="WC1N 3XX", country="UK")
        ]
        session.add_all(addresses)
        await session.commit()

        # Step 2: Seed Orders
        orders = [
            Order(id=uuid.UUID("dddddddd-dddd-dddd-dddd-dddddddddddd"), customer_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", created_at=datetime.now(timezone.utc), status=OrderStatus.PENDING, items=[
                OrderItem(id=uuid.UUID("11111111-aaaa-4444-bbbb-aaaaaaaaaaaa"), product_id=uuid.UUID("11111111-aaaa-4444-bbbb-111111111111"), quantity=2, unit_price=Decimal("129.99")),
                OrderItem(id=uuid.UUID("22222222-bbbb-4444-cccc-bbbbbbbbbbbb"), product_id=uuid.UUID("22222222-bbbb-4444-cccc-222222222222"), quantity=1, unit_price=Decimal("299.99")),
                OrderItem(id=uuid.UUID("33333333-cccc-4444-dddd-cccccccccccc"), product_id=uuid.UUID("33333333-cccc-4444-dddd-333333333333"), quantity=3, unit_price=Decimal("199.99"))
            ]),
            Order(id=uuid.UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"), customer_id="44444444-4444-4444-4444-444444444444", created_at=datetime.now(timezone.utc), status=OrderStatus.PENDING, items=[
                OrderItem(id=uuid.UUID("44444444-aaaa-4444-bbbb-aaaaaaaaaaaa"), product_id=uuid.UUID("44444444-aaaa-4444-bbbb-444444444444"), quantity=5, unit_price=Decimal("49.99")),
                OrderItem(id=uuid.UUID("55555555-bbbb-4444-cccc-bbbbbbbbbbbb"), product_id=uuid.UUID("55555555-bbbb-4444-cccc-555555555555"), quantity=2, unit_price=Decimal("89.99"))
            ]),
            Order(id=uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"), customer_id="55555555-5555-5555-5555-555555555555", created_at=datetime.now(timezone.utc), status=OrderStatus.PENDING, items=[
                OrderItem(id=uuid.UUID("66666666-aaaa-4444-bbbb-aaaaaaaaaaaa"), product_id=uuid.UUID("66666666-aaaa-4444-bbbb-666666666666"), quantity=1, unit_price=Decimal("999.99")),
                OrderItem(id=uuid.UUID("77777777-bbbb-4444-cccc-bbbbbbbbbbbb"), product_id=uuid.UUID("77777777-bbbb-4444-cccc-777777777777"), quantity=10, unit_price=Decimal("9.99"))
            ])
        ]
        for order in orders:
            order.total_amount = sum(item.unit_price * item.quantity for item in order.items)
        session.add_all(orders)
        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(initialize_database())
