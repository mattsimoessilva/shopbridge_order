import aiohttp
import json
from typing import Any, Dict, Optional

class LogisticsServiceClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session: None

    async def __aenter__(self) -> "LogisticsServiceClient":
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def create_shipment(
        self,
        order_id: str,
        status: str,
        dispatchDate: Optional[str],
        carrier: str,
        serviceLevel: str,
        street: str,
        city: str,
        state: str,
        postalCode: str,
        country: str,
    ) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/shipments"
        payload = {
            "orderId": order_id,
            "status": status,
            "dispatchDate": dispatchDate,
            "carrier": carrier,
            "serviceLevel": serviceLevel,
            "street": street,
            "city": city,
            "state": state,
            "postalCode": postalCode,
            "country": country,
        }

        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            text_body = await resp.text()
            if resp.status != 201:
                raise RuntimeError(f"Error creating shipment: {resp.status} - {text_body}")
            if text_body and resp.headers.get("Content-Type", "").startswith("application/json"):
                return json.loads(text_body)
            return {}

    async def get_shipment(self, shipment_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/shipments/{shipment_id}"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            text_body = await resp.text()
            if resp.status == 404:
                raise ValueError(f"Shipment {shipment_id} not found.")
            elif resp.status != 200:
                raise RuntimeError(f"Error fetching shipment: {resp.status} - {text_body}")
            return await resp.json()

    async def update_shipment(self, shipment_id: str, status: str) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/shipments/{shipment_id}/status"
        payload = {"status": status}
        async with session.patch(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            text_body = await resp.text()
            if resp.status == 404:
                raise ValueError(f"Shipment {shipment_id} not found.")
            elif resp.status != 200:
                raise RuntimeError(f"Error updating shipment: {resp.status} - {text_body}")

    async def check_availability(
        self,
        street: str,
        city: str,
        state: str,
        postalCode: str,
        country: str,
    ) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/shipping/availability"
        payload = {
            "street": street,
            "city": city,
            "state": state,
            "postalCode": postalCode,
            "country": country,
        }
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            text_body = await resp.text()
            if resp.status == 400:
                raise ValueError(f"Bad request: {text_body}")
            elif resp.status == 500:
                raise RuntimeError(f"Server error: {text_body}")
            elif resp.status not in (200, 201):
                raise RuntimeError(f"Unexpected status {resp.status}: {text_body}")
            if text_body and resp.headers.get("Content-Type", "").startswith("application/json"):
                return json.loads(text_body)
            return {}
