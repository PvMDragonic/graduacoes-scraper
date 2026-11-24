from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from lxml import html

class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.driver = Driver(
            binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            headless = False,
            uc = True
        )

    def fetch(self, url: str):
        def page_state(driver):
            if driver.find_elements(By.CLASS_NAME, "col-md-12"):
                return "found"
            if driver.execute_script("return document.readyState") == "complete":
                return "missing"
            return False # Página carregando; espera.
        
        try:
            self.driver.get(url)
            state = WebDriverWait(self.driver, 30).until(page_state)

            if state == "missing":
                return None

            return html.fromstring(self.driver.page_source)

        except Exception as e:
            return e

    def parse(self, tree) -> str:
        hasTarget = tree.xpath("boolean(//fieldset[contains(., 'PSICOLOGIA')])")
        return self.base_url if hasTarget else ''

    def scrape(self):
        tree = self.fetch(self.base_url)
        return self.parse(tree)

    def close(self):
        self.driver.quit()