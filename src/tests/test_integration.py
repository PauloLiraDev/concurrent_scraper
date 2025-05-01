import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from unittest.mock import patch
from src.automation.app import app


@pytest.mark.asyncio
async def test_scrape_endpoint_with_category():
    """Test for scraping products from a specific category."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/scrape?category=Electronics")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        for product in response.json():
            assert "id" in product
            assert "name" in product
            assert "category" in product
            assert "price" in product
            assert "stock" in product
            assert product["category"] == "Electronics"


@pytest.mark.asyncio
async def test_scrape_endpoint_without_category():
    """Test for scraping products without specifying a category."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/scrape")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        # Verifica se há itens de várias categorias
        categories = {product["category"] for product in response.json()}
        assert len(categories) > 0


@pytest.mark.asyncio
async def test_scrape_endpoint_error():
    """Test for handling errors during scraping."""
    with patch("src.executer.service.ScrapingService.scrape_category") as mock_scrape:
        # Simulate an error in the scraping process
        mock_scrape.side_effect = Exception("Test error")
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/scrape?category=Invalid")
            assert response.status_code == 500
            assert response.json() == {"detail": "Internal Server Error"}
