# tests/conftest.py
import sys
import os
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from asgiref.wsgi import WsgiToAsgi
import pytest_asyncio
from flask import g, current_app
from types import SimpleNamespace

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app  # Import your app factory


@pytest_asyncio.fixture
async def client_with_mocked_address_service():
    app = create_app()

    # Create a pure mock service with async methods
    mock_service = SimpleNamespace(
        CreateAsync=AsyncMock(),
        GetAllAsync=AsyncMock(),
        GetByIdAsync=AsyncMock(),
        UpdateAsync=AsyncMock(),
        DeleteAsync=AsyncMock()
    )

    @app.before_request
    def inject_service_and_db():
        g.db = MagicMock()  # Fake DB session
        current_app.extensions["address_service"] = mock_service

    asgi_app = WsgiToAsgi(app)
    async with AsyncClient(
        transport=ASGITransport(app=asgi_app),
        base_url="http://test"
    ) as client:
        yield client, mock_service



@pytest_asyncio.fixture
async def client_with_mocked_order_service():
    app = create_app()

    # Create a pure mock service with async methods
    mock_service = SimpleNamespace(
        CreateAsync=AsyncMock(),
        GetAllAsync=AsyncMock(),
        GetByIdAsync=AsyncMock(),
        UpdateAsync=AsyncMock(),
        DeleteAsync=AsyncMock()
    )

    @app.before_request
    def inject_service_and_db():
        g.db = MagicMock()  # Fake DB session
        current_app.extensions["order_service"] = mock_service

    asgi_app = WsgiToAsgi(app)
    async with AsyncClient(
        transport=ASGITransport(app=asgi_app),
        base_url="http://test"
    ) as client:
        yield client, mock_service
