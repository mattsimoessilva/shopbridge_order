import aiohttp
import asyncio
from typing import Any, Dict, Optional


class ProductServiceClient:

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
            if self._session and not self._session.closed:
                await self._session.close()

            self._session = aiohttp.ClientSession()
            self._loop = loop

        return self._session
    
    # Product Endpoints region

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/products/{product_id}"

        async with session.get(url, timeout=5) as resp:
            if resp.status == 404:
                raise ValueError(f"Product {product_id} not found.")

            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching product: {resp.status} - {text}")

            return await resp.json()

    async def reserve_product_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/products/{product_id}/reserve"

        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reserving product stock: {resp.status} - {text}")


    async def release_product_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/products/{product_id}/release"

        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error releasing product stock: {resp.status} - {text}")


    async def reduce_product_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/products/{product_id}/reduce"

        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reducing product stock: {resp.status} - {text}")

    # endregion

    # Product Variant Endpoints

    async def get_variant(self, product_variant_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/product-variants/{product_variant_id}"

        async with session.get(url, timeout=5) as resp:
            if resp.status == 404:
                raise ValueError(f"Product Variant {product_variant_id} not found.")

            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching product variant: {resp.status} - {text}")

            return await resp.json()

    async def reserve_variant_stock(self, variant_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/product-variants/{variant_id}/reserve"

        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reserving variant stock: {resp.status} - {text}")


    async def release_variant_stock(self, variant_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/product-variants/{variant_id}/release"

        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error releasing variant stock: {resp.status} - {text}")


    async def reduce_variant_stock(self, variant_id: str, quantity: int) -> None:
        session = await self._get_session()
        url = f"{self._base_url}/product-variants/{variant_id}/reduce"

        async with session.post(url, json={"quantity": quantity}, timeout=5) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reducing variant stock: {resp.status} - {text}")

    # endregion

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
