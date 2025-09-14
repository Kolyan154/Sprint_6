import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации и закрытия драйвера Chrome.
    """
    try:
        service = Service(ChromeDriverManager().install())
    except Exception:
        service = Service()  # Используем системный chromedriver

    options = Options()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()