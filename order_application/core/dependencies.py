from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core import async_session_factory
from repositories import OrderRepository, AddressRepository
from services import OrderService, AddressService
from clients import ProductServiceClient, LogisticsServiceClient

# --- Database Session Dependency ---
async def get_database() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

# --- Repository Dependencies ---
def get_order_repository(request: Request) -> OrderRepository:
    return request.app.state.order_repository

def get_address_repository(request: Request) -> AddressRepository:
    return request.app.state.address_repository

# --- Client Dependencies ---
def get_product_client(request: Request) -> ProductServiceClient:
    return request.app.state.product_client

def get_logistics_client(request: Request) -> LogisticsServiceClient:
    return request.app.state.logistics_client

# --- Service Dependencies ---
def get_order_service(request: Request) -> OrderService:
    return request.app.state.order_service

def get_address_service(request: Request) -> AddressService:
    return request.app.state.address_service
