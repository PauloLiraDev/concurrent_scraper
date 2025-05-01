from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.log import get_logger
from src.executer.service import ScrapingService
from src.builder.pool import WebDriverPool
from src.models.product import Product


pool = WebDriverPool()
service = ScrapingService(pool)
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of the application."""
    # Setup phase - executed on application startup
    yield
    # Cleanup phase - executed on application shutdown
    logger.info("Shutting down WebDriverPool...")
    pool.shutdown()
    logger.info("WebDriverPool shut down successfully.")


app = FastAPI(lifespan=lifespan)


@app.get("/scrape", response_model=list[Product])
async def scrape(category: str | None = None):
    """
    Endpoint to scrape products from the specified category.
    
    Args:
        category (Optional[str]): The category to scrape products from
        
    Returns:
        list[Product]: List of products from the specified category
        
    Raises:
        HTTPException: If an error occurs during the scraping process
    """
    logger.info(f"Received scrape request for category: {category or 'all'}")
    try:
        # Use the ScrapingService to scrape the category
        products = await service.scrape_category(category)
        return products
    except HTTPException as e:
        logger.warning(f"Scraping error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    