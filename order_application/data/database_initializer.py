import asyncio
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.entities import Base
from models.entities import Address
from models.entities import Order
from models.entities import OrderItem
from models.enums import OrderStatus


async def initialize_database():
    engine = create_async_engine("sqlite+aiosqlite:///./database.db", echo=True, future=True)
    async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:

        # Seed Addresses inline
        session.add_all([
            Address(id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", customer_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", street="Avenida Paulista, 1578", city="São Paulo", state="SP", postal_code="01310-200", country="Brasil"),
            Address(id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", customer_id="44444444-4444-4444-4444-444444444444", street="Rua das Flores, 45", city="Curitiba", state="PR", postal_code="80020-090", country="Brasil"),
            Address(id="cccccccc-cccc-cccc-cccc-cccccccccccc", customer_id="55555555-5555-5555-5555-555555555555", street="Praia de Botafogo, 300", city="Rio de Janeiro", state="RJ", postal_code="22250-040", country="Brasil")
        ])
        await session.commit()

        # Seed Orders and OrderItems inline
        session.add_all([
            Order(id="dddddddd-dddd-dddd-dddd-dddddddddddd", customer_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", created_at=datetime.now(timezone.utc), status=OrderStatus.PENDING, total_amount=Decimal("259.98"), items=[OrderItem(id="11111111-aaaa-4444-bbbb-aaaaaaaaaaaa", product_id="11111111-aaaa-4444-bbbb-111111111111", quantity=2, unit_price=Decimal("129.99"))]),
            Order(id="eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee", customer_id="44444444-4444-4444-4444-444444444444", created_at=datetime.now(timezone.utc), status=OrderStatus.PENDING, total_amount=Decimal("1749.95"), items=[OrderItem(id="44444444-aaaa-4444-bbbb-aaaaaaaaaaaa", product_id="22222222-bbbb-4444-cccc-222222222222", quantity=5, unit_price=Decimal("349.99"))]),
            Order(id="ffffffff-ffff-ffff-ffff-ffffffffffff", customer_id="55555555-5555-5555-5555-555555555555", created_at=datetime.now(timezone.utc), status=OrderStatus.PENDING, total_amount=Decimal("249.99"), items=[OrderItem(id="66666666-aaaa-4444-bbbb-aaaaaaaaaaaa", product_id="33333333-cccc-4444-dddd-333333333333", quantity=1, unit_price=Decimal("249.99"))])
        ])
        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(initialize_database())
