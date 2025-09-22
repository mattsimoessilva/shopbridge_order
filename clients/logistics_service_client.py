import aiohttp
import asyncio
from typing import Any, Dict, Optional
import json


class LogisticsServiceClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        loop = asyncio.get_running_loop()
        if (
            self._session is None
            or self._session.closed
            or self._loop is not loop
        ):
            # Close old session if it exists
            if self._session and not self._session.closed:
                await self._session.close()
            self._session = aiohttp.ClientSession()
            self._loop = loop
        return self._session

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
        country: str
    ) -> Dict[str, Any]:
        """
        Create a shipment request matching ShipmentCreateDTO.
        """
        session = await self._get_session()
        url = f"{self._base_url}/Shipment"
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
            "country": country
        }

        async with session.post(url, json=payload, timeout=5) as r:
            status_code = r.status
            headers = r.headers
            text_body = await r.text()

            print(status_code)
            print(headers)
            print(text_body)

            if status_code != 201:
                raise RuntimeError(f"Error creating shipment: {status_code} - {text_body}")

            # Only parse JSON if there is a body and the content type is JSON
            if text_body.strip() and headers.get("Content-Type", "").startswith("application/json"):
                return json.loads(text_body)

            return {}



    async def get_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """
        Retrieve shipment status/details.
        """
        session = await self._get_session()
        url = f"{self._base_url}/Shipment/{shipment_id}"
        async with session.get(url, timeout=5) as resp:
            if resp.status == 404:
                raise ValueError(f"Shipment {shipment_id} not found.")
            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching shipment: {resp.status} - {text}")
            return await resp.json()

    async def update_shipment(self, shipment_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update shipment details (e.g., address change before dispatch).
        """
        session = await self._get_session()
        url = f"{self._base_url}/Shipment/{shipment_id}"
        async with session.patch(url, json=updates, timeout=5) as resp:
            if resp.status == 404:
                raise ValueError(f"Shipment {shipment_id} not found.")
            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error updating shipment: {resp.status} - {text}")
            return await resp.json()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
