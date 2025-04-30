import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.executer.service import ScrapingService
from src.builder.pool import WebDriverPool
from src.models.product import Product


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


pool = WebDriverPool()
service = ScrapingService(pool)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.info("Shutting down WebDriverPool...")
    pool.shutdown()
    logger.info("WebDriverPool shut down successfully.")

app = FastAPI(lifespan=lifespan)

@app.get("/scrape", response_model=list[Product])
async def scrape(category: Optional[str]):
    """
    Endpoint to scrape products from the specified category.
    """
    logger.info(f"Received scrape request for category: {category}")
    try:
        # In this line, we are using the ScrapingService to scrape the category.
        products = await service.scrape_category(category)
        return products
    except HTTPException as e:
        logger.warning(f"Scraping error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")