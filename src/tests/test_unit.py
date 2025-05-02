import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.builder.pool import WebDriverPool
from src.executer.service import ScrapingService
from fastapi import HTTPException


# Fixture for the Scraper mock
@pytest.fixture
def mock_scraper():
    scraper = Mock()
    sample_products = [
        {
            "id": "1",
            "name": "Test Product",
            "category": "Electronics",
            "price": "$199.99",
            "stock": "In Stock (5)",
        }
    ]
    scraper.scrape_category.return_value = sample_products
    return scraper


@patch("src.builder.pool.Scraper")
def test_webdriver_pool_init(MockScraper):
    """
    Test for WebDriverPool initialization with mocked Scraper
    """
    # Configure the mock
    mock_instance = MockScraper.return_value
    mock_instance.scrape_category.return_value = [
        {
            "id": "1",
            "name": "Test",
            "category": "Test",
            "price": "$10.00",
            "stock": "In Stock (5)",
        }
    ]

    # Create the pool with the mock
    with patch("src.settings.POOL_SIZE", 4):
        pool = WebDriverPool()

    # Verify the pool was initialized correctly
    assert pool.queue.qsize() == 4
    assert len(pool.workers) == 4


@pytest.mark.asyncio
async def test_scraping_service():
    """
    Test for ScrapingService with available workers
    """

    mock_pool = Mock()
    mock_products = [
        {
            "id": "1",
            "name": "Test",
            "category": "Test",
            "price": "$10",
            "stock": "In Stock (5)",
        }
    ]

    mock_pool.has_available_worker.return_value = True

    mock_pool.scrape_async = AsyncMock(return_value=mock_products)

    # Create service with the mocked pool
    service = ScrapingService(pool=mock_pool)

    # Test the scrape_category method
    result = await service.scrape_category("Electronics")
    assert result == mock_products
    mock_pool.scrape_async.assert_called_once_with("Electronics")


@pytest.mark.asyncio
async def test_scraping_service_no_workers():
    """
    Test for the case when no workers are available
    """

    mock_pool = Mock()
    mock_pool.has_available_worker.return_value = False

    service = ScrapingService(pool=mock_pool)

    with pytest.raises(HTTPException) as excinfo:
        await service.scrape_category("Electronics")

    assert excinfo.value.status_code == 429
