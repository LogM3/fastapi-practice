from app.request_test.schema import TestJson
from httpx import AsyncClient


class RequestService:
    url: str = 'https://jsonplaceholder.typicode.com/posts'

    async def get(self) -> list[TestJson]:
        try:
            async with AsyncClient() as client:
                response = await client.get(self.url)
            return [TestJson.model_validate(item) for item in response.json()]
        except Exception:
            return []
