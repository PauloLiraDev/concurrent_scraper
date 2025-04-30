# builder/pool.py
import threading
import queue
import asyncio
from src.settings import POOL_SIZE
from src.builder.scraper import Scraper

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

    def scrape(self, category: str):
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
        # for worker in self.workers:
        #     worker.driver.close()
        self.queue.queue.clear()
        self.workers.clear()