import os
from dotenv import load_dotenv

load_dotenv()

POOL_SIZE = int(os.getenv("POOL_SIZE", 1))
WAIT_TIME = int(os.getenv("WAIT_TIME", 5))
CHROME_OPTIONS = ["--disable-gpu", "--no-sandbox"]
TARGET_URL = "https://selenium-html-test.replit.app/"
