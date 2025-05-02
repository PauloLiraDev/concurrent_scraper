from fastapi import HTTPException
from typing import List
from src.builder.pool import WebDriverPool
from src.models.product import Product


class ScrapingService:
    def __init__(self, pool: WebDriverPool):
        self.pool = pool

    async def scrape_category(self, category: str) -> List[Product]:
        """
        Scrape products from a specific category using the WebDriver pool.
        Args:
            category (str): The category to scrape.
        Returns:
            List[Product]: A list of products in the specified category.
        Raises:
            HTTPException: If no worker is available in the pool.
        """

        # Check if there is an available worker in the pool
        if not self.pool.has_available_worker():
            raise HTTPException(
                status_code=429, detail="No worker available, try again later."
            )

        products = await self.pool.scrape_async(category)
        return products
