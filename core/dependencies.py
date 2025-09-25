# dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import async_session_factory
from repositories.order_repository_impl import OrderRepository
from repositories.address_repository_impl import AddressRepository
from services.order_service_impl import OrderService
from services.address_service_impl import AddressService
from clients.product_service_client import ProductServiceClient
from clients.logistics_service_client import LogisticsServiceClient

# Provide a database session
async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

# Provide OrderRepository
def get_order_repository() -> OrderRepository:
    # You could pass a session factory if your repo needs it
    return OrderRepository(session_factory=None)

# Provide AddressRepository
def get_address_repository() -> AddressRepository:
    return AddressRepository(session_factory=None)

# Provide ProductServiceClient
def get_product_client() -> ProductServiceClient:
    return ProductServiceClient(base_url="http://localhost:5000/")  # adjust base_url

# Provide LogisticsServiceClient
def get_logistics_client() -> LogisticsServiceClient:
    return LogisticsServiceClient(base_url="http://localhost:8000/")  # adjust base_url

# Provide OrderService
async def get_order_service(
    db: AsyncSession = Depends(get_db),
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

# Provide AddressService
async def get_address_service(
    db: AsyncSession = Depends(get_db),
    repo: AddressRepository = Depends(get_address_repository),
) -> AddressService:
    service = AddressService(repository=repo)
    return service
