from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

TARGET_URL = "https://selenium-html-test.replit.app/"

# Configurações do Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Descomente se quiser rodar em modo headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

# Inicializa o Chrome com o driver gerenciado automaticamente
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Visita o site
driver.get(TARGET_URL)

# Espera um pouco para visualização
time.sleep(5)

# Fecha o navegador
driver.quit()
