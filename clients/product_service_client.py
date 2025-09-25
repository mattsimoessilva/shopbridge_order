import aiohttp
from typing import Any, Dict, Optional

class ProductServiceClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None

    async def open(self) -> "ProductServiceClient":
        return await self.__aenter__()

    async def __aenter__(self) -> "ProductServiceClient":
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

    # ---------------- Product Endpoints ----------------

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/products/{product_id}"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            text_body = await resp.text()
            if resp.status == 404:
                raise ValueError(f"Product {product_id} not found.")
            elif resp.status != 200:
                raise RuntimeError(f"Error fetching product: {resp.status} - {text_body}")
            return await resp.json()

    async def reserve_product_stock(self, product_id: str, quantity: int) -> None:
        await self._modify_stock(f"{self._base_url}/products/{product_id}/reserve", quantity)

    async def release_product_stock(self, product_id: str, quantity: int) -> None:
        await self._modify_stock(f"{self._base_url}/products/{product_id}/release", quantity)

    async def reduce_product_stock(self, product_id: str, quantity: int) -> None:
        await self._modify_stock(f"{self._base_url}/products/{product_id}/reduce", quantity)

    # ---------------- Variant Endpoints ----------------

    async def get_variant(self, variant_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}/product-variants/{variant_id}"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            text_body = await resp.text()
            if resp.status == 404:
                raise ValueError(f"Product Variant {variant_id} not found.")
            elif resp.status != 200:
                raise RuntimeError(f"Error fetching product variant: {resp.status} - {text_body}")
            return await resp.json()

    async def reserve_variant_stock(self, variant_id: str, quantity: int) -> None:
        await self._modify_stock(f"{self._base_url}/product-variants/{variant_id}/reserve", quantity)

    async def release_variant_stock(self, variant_id: str, quantity: int) -> None:
        await self._modify_stock(f"{self._base_url}/product-variants/{variant_id}/release", quantity)

    async def reduce_variant_stock(self, variant_id: str, quantity: int) -> None:
        await self._modify_stock(f"{self._base_url}/product-variants/{variant_id}/reduce", quantity)

    # ---------------- Private helper ----------------

    async def _modify_stock(self, url: str, quantity: int) -> None:
        session = await self._get_session()
        async with session.post(url, json={"quantity": quantity}, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            text_body = await resp.text()
            if resp.status != 200:
                raise RuntimeError(f"Error modifying stock at {url}: {resp.status} - {text_body}")
