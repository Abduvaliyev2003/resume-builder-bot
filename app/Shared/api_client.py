import httpx

from app.Shared.config import settings

class APIClient:

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=settings.API_URL,
            timeout=settings.REQUEST_TIMEOUT,
        )
    async def get(self, url: str, headers=None) -> httpx.Response:
        response = await self.client.get(url, headers=headers)

        response.raise_for_status()

        return response.json()

    async def post(self, url: str, data: None, headers=None) -> httpx.Response:
        response = await self.client.post(url, json=data, headers=headers)

        response.raise_for_status()

        return response.json()

    async def put(self, url: str, data: None, headers=None) -> httpx.Response:
        response = await self.client.put(url, json=data, headers=headers)

        response.raise_for_status()

        return response.json()

    async def delete(self, url: str, headers=None) -> httpx.Response:
        response = await self.client.delete(url, headers=headers)

        response.raise_for_status()

        return response.json()

api = APIClient()
