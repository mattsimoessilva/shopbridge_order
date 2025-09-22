import aiohttp
from typing import Any, Dict

class ProductServiceClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/Product/{product_id}"
        async with session.get(url, timeout=5) as resp:
            if resp.status == 404:
                raise ValueError(f"Product {product_id} not found.")
            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching product: {resp.status} - {text}")
            return await resp.json()

    async def get_variant(self, product_id: str, variant_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/Product/{product_id}/variants/{variant_id}"
        async with session.get(url, timeout=5) as resp:
            if resp.status == 404:
                raise ValueError(f"Variant {variant_id} for product {product_id} not found.")
            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching variant: {resp.status} - {text}")
            return await resp.json()

    async def reserve_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/Product/{product_id}/reserve"
        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reserving stock: {resp.status} - {text}")

    async def release_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/Product/{product_id}/release"
        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error releasing stock: {resp.status} - {text}")

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
