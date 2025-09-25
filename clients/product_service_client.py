import aiohttp
from typing import Any, Dict, Optional


class ProductServiceClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self


    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def open(self):
        return await self.__aenter__()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            raise RuntimeError("ProductServiceClient is not open or already closed.")
        return self._session

    # ---------------- Product Endpoints ----------------

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        async with session.get(f"/products/{product_id}") as resp:
            if resp.status == 404:
                raise ValueError(f"Product {product_id} not found.")
            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching product: {resp.status} - {text}")
            return await resp.json()

    async def reserve_product_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(f"/products/{product_id}/reserve", json={"quantity": quantity}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reserving product stock: {resp.status} - {text}")

    async def release_product_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(f"/products/{product_id}/release", json={"quantity": quantity}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error releasing product stock: {resp.status} - {text}")

    async def reduce_product_stock(self, product_id: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(f"/products/{product_id}/reduce", json={"quantity": quantity}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reducing product stock: {resp.status} - {text}")

    # ---------------- Variant Endpoints ----------------

    async def get_variant(self, product_variant_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        async with session.get(f"/product-variants/{product_variant_id}") as resp:
            if resp.status == 404:
                raise ValueError(f"Product Variant {product_variant_id} not found.")
            elif resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error fetching product variant: {resp.status} - {text}")
            return await resp.json()

    async def reserve_variant_stock(self, variant_id: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(f"/product-variants/{variant_id}/reserve", json={"quantity": quantity}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reserving variant stock: {resp.status} - {text}")

    async def release_variant_stock(self, variant_id: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(f"/product-variants/{variant_id}/release", json={"quantity": quantity}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error releasing variant stock: {resp.status} - {text}")

    async def reduce_variant_stock(self, variant_id: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(f"/product-variants/{variant_id}/reduce", json={"quantity": quantity}) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Error reducing variant stock: {resp.status} - {text}")