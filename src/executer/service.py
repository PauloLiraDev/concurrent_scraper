from fastapi import HTTPException
from typing import List
from src.builder.pool import WebDriverPool
from src.models.product import Product

class ScrapingService:
    def __init__(self, pool: WebDriverPool):
        self.pool = pool

    async def scrape_category(self, category: str) -> List[Product]:
        if not self.pool.has_available_worker():
            raise HTTPException(status_code=429, detail="no worker available")
        
        products = await self.pool.scrape_async(category)
        return products