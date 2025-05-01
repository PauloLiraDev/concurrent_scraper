import os
from dotenv import load_dotenv

load_dotenv()

POOL_SIZE = int(os.getenv("POOL_SIZE", 4))
WAIT_TIME = int(os.getenv("WAIT_TIME", 5))
CHROME_OPTIONS = [
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
]
TARGET_URL = "https://selenium-html-test.replit.app/"
