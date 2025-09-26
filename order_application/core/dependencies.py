from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import async_session_factory
from repositories import OrderRepository
from repositories import AddressRepository
from services import OrderService
from services import AddressService
from clients import ProductServiceClient
from clients import LogisticsServiceClient


# --- Database Session Dependency ---
async def get_database() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


# --- Repository Dependencies ---
def get_order_repository() -> OrderRepository:
    return OrderRepository(session_factory=None)


def get_address_repository() -> AddressRepository:
    return AddressRepository(session_factory=None)


# --- Client Dependencies ---
def get_product_client() -> ProductServiceClient:
    return ProductServiceClient(base_url="http://localhost:5000/api/")  # adjust base_url


def get_logistics_client() -> LogisticsServiceClient:
    return LogisticsServiceClient(base_url="http://localhost:8000/api/")  # adjust base_url


# --- Service Dependencies ---
async def get_order_service(
    db: AsyncSession = Depends(get_database),
    repo: OrderRepository = Depends(get_order_repository),
    addr_repo: AddressRepository = Depends(get_address_repository),
    product_client: ProductServiceClient = Depends(get_product_client),
    logistics_client: LogisticsServiceClient = Depends(get_logistics_client),
) -> OrderService:

    service = OrderService(
        repository=repo,
        address_repository=addr_repo,
        product_client=product_client,
        logistics_client=logistics_client
    )

    return service


async def get_address_service(
    db: AsyncSession = Depends(get_database),
    repo: AddressRepository = Depends(get_address_repository),
) -> AddressService:

    service = AddressService(repository=repo)

    return service
