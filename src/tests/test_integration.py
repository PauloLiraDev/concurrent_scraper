import pytest
from httpx import AsyncClient
from automation.app import api

@pytest.mark.asyncio
async def test_scrape_endpoint():
    async with AsyncClient(app=api, base_url="http://test") as client:
        response = await client.get("/scrape?category=Accessories")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        for product in response.json():
            assert "title" in product
            assert "price" in product
            assert "rating" in product
            assert "link" in product
            assert isinstance(product["title"], str)
            assert isinstance(product["price"], (float, int))
            assert isinstance(product["rating"], (float, int))
            assert isinstance(product["link"], str)