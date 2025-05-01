import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.builder.pool import WebDriverPool
from src.executer.service import ScrapingService
from fastapi import HTTPException

# Mock para o Scraper
@pytest.fixture
def mock_scraper():
    scraper = Mock()
    sample_products = [
        {
            "id": "1",
            "name": "Test Product",
            "category": "Electronics",
            "price": "$199.99",
            "stock": "10"
        }
    ]
    scraper.scrape_category.return_value = sample_products
    return scraper

# Test para o WebDriverPool
@patch('src.builder.pool.Scraper')
def test_webdriver_pool_init(MockScraper):
    # Configura o mock
    mock_instance = MockScraper.return_value
    mock_instance.scrape_category.return_value = [{"id": "1", "name": "Test", "category": "Test", "price": "$10.00", "stock": "In Stock (5)"}]
    
    # Cria o pool com o mock
    with patch('src.settings.POOL_SIZE', 4):
        pool = WebDriverPool()
    
    # Verifica se o pool foi inicializado corretamente
    assert pool.queue.qsize() == 4
    assert len(pool.workers) == 4

# Test para o ScrapingService
@pytest.mark.asyncio
async def test_scraping_service():
    # Cria mocks - use Mock() para has_available_worker normal e configure apenas scrape_async como async
    mock_pool = Mock()
    mock_products = [{"id": "1", "name": "Test", "category": "Test", "price": "$10", "stock": "5"}]
    
    # Configure has_available_worker como método normal (não assíncrono)
    mock_pool.has_available_worker.return_value = True
    # Configure o método assíncrono scrape_async 
    mock_pool.scrape_async = AsyncMock(return_value=mock_products)
    
    # Cria o serviço com o pool mockado
    service = ScrapingService(pool=mock_pool)
    
    # Testa o método scrape_category
    result = await service.scrape_category("Electronics")
    assert result == mock_products
    mock_pool.scrape_async.assert_called_once_with("Electronics")

# Test para o caso de não ter workers disponíveis
@pytest.mark.asyncio
async def test_scraping_service_no_workers():
    # Cria mocks
    mock_pool = Mock()
    mock_pool.has_available_worker.return_value = False

    service = ScrapingService(pool=mock_pool)
    
    # Testa o método scrape_category quando não há workers disponíveis
    with pytest.raises(HTTPException) as excinfo:
        await service.scrape_category("Electronics")
        
    assert excinfo.value.status_code == 429
    assert excinfo.value.detail == "no worker available"