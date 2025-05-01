# builder/pool.py
import threading
import queue
import asyncio
from src.settings import POOL_SIZE
from src.builder.scraper import Scraper
from src.log import get_logger

# Initialize the logger for this module
logger = get_logger()


class WebDriverPool:
    def __init__(self):
        self.lock = threading.Lock()
        self.queue = queue.Queue(maxsize=POOL_SIZE)
        self.workers = []

        for i in range(POOL_SIZE):
            scraper = Scraper()
            self.queue.put(scraper)
            self.workers.append(scraper)

    def has_available_worker(self) -> bool:
        return not self.queue.empty()

    def scrape(self, category: str | None):
        """
        Obtains a scraper from the pool, uses it to scrape the given category, and returns it to the pool.

        This method implements the resource pool pattern, allowing reuse of expensive WebDriver
        instances while limiting concurrency to the configured pool size.

        Args:
            category (str|None): The category to scrape. If None, scrapes all categories.

        Returns:
            list[Product]: A list of products from the specified category.

        Note:
            This is a blocking operation. For non-blocking behavior, use scrape_async instead.
        """
        scraper = self.queue.get()
        try:
            return scraper.scrape_category(category)
        finally:
            self.queue.put(scraper)

    async def scrape_async(self, category: str):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.scrape, category)

    def shutdown(self):
        """Shut down all workers in the pool."""
        try:
            # Close all webdriver instances
            for worker in self.workers:
                try:
                    worker.driver.quit()  # Use quit() instead to ensure full cleanup
                    logger.info("Successfully closed WebDriver instance")
                except Exception as e:
                    logger.error(f"Error closing WebDriver: {e}")
        finally:
            # Clear queues and lists
            self.queue.queue.clear()
            self.workers.clear()
            logger.info("WebDriver pool resources cleared")
