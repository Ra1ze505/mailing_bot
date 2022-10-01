from typing import AsyncGenerator

import httpx


async def init_async_http_client(base_url: str) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Инициализация асинхронного http-клиента"""
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield client
