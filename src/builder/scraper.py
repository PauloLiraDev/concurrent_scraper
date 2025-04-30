from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from src.models.product import Product
from src.settings import CHROME_OPTIONS, TARGET_URL, WAIT_TIME

class Scraper:
    def __init__(self):
        options = Options()
        for arg in CHROME_OPTIONS:
            options.add_argument(arg)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=service,
            options=options
        )
        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def scrape_category(self, category: str) -> list[Product]:
        """
        Scrape the products from a specific category.
        Args:
            category (str): The category to scrape.
        Returns:
            list[Product]: A list of products in the specified category.
        """

        self.driver.get(f"{TARGET_URL}")

        # Wait the category dropdown to be clickable
        self.wait.until(EC.element_to_be_clickable((By.ID, "category-filter"))).click()

        # Click on span with the category name
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{category.title()}']"))).click()
        
        
        

        products = self.get_products()
        
        # Pagination logic:
        pagination_range_end = self.wait.until(EC.element_to_be_clickable((By.ID, "pagination-range-end")))
        pagination_range_total = self.wait.until(EC.element_to_be_clickable((By.ID, "pagination-total")))
        while pagination_range_end.text != pagination_range_total.text:
            # Click on the next page
            self.wait.until(EC.element_to_be_clickable((By.ID, "next-page"))).click()
            # Wait for the next page to load
            self.wait.until(EC.presence_of_element_located((By.ID, "product-table")))
            products += self.get_products()
            # Update the pagination range end
            pagination_range_end = self.wait.until(EC.element_to_be_clickable((By.ID, "pagination-range-end")))

        return products
    
    def get_products(self) -> list[Product]:
        """
        Get the products from the current page.
        Returns:
            list[Product]: A list of products on the current page.
        """
        
        products = []

        # Wait for the product table to be present
        table = self.wait.until(EC.presence_of_element_located((By.ID, "product-table")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_values = [cell.text for cell in cells]
            if cell_values and any(cell_values): # only add non-empty rows
                prod_info_dict = {
                    "id": cell_values[0],
                    "name": cell_values[1],
                    "category": cell_values[2],
                    "price": cell_values[3],
                    "stock": cell_values[4],
                }
                products.append(prod_info_dict)
        return products
