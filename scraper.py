from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from functools import cache
from lxml import html
import winreg
import os

@cache # Salva o retorno dessa função após a primeira execução.
def find_browser() -> str:
    candidates = [
        ("chrome.exe", r"Google\Chrome\Application\chrome.exe"),
        ("brave.exe", r"BraveSoftware\Brave-Browser\Application\brave.exe"),
    ]

    for exe, relative_path in candidates:
        # Windows registra os navegadores instalados em "App Paths".
        for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                key_path = rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{exe}"
                with winreg.OpenKey(hive, key_path) as key:
                    path = winreg.QueryValue(key, None).strip('"')
                    if os.path.isfile(path):
                        return path
            except OSError:
                pass

        # Tenta as pastas de instalação padrão.
        for base in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
            folder = os.environ.get(base)
            if folder:
                path = os.path.join(folder, relative_path)
                if os.path.isfile(path):
                    return path

    # "Chrome for Testing" como backup final.
    return "cft"

class Scraper:
    def __init__(self, major: str):
        self.driver = Driver(
            binary_location = find_browser(),
            headless = False,
            uc = True
        )
        self.driver.set_page_load_timeout(30)
        self.major = major

    def fetch(self, url: str):
        def page_state(driver):
            if driver.find_elements(By.CLASS_NAME, "col-md-12"):
                return "found"
            title = driver.title.lower()
            if "just a moment" in title or "um momento" in title:
                return False  # Desafio do Cloudflare; espera.
            if driver.execute_script("return document.readyState") == "complete":
                return "missing"
            return False # Página carregando; espera.
        
        try:
            self.driver.default_get(url)
            state = WebDriverWait(self.driver, 30).until(page_state)

            if state == "missing":
                return None

            return html.fromstring(self.driver.page_source)

        except Exception as e:
            print(f"Erro em {url}: {e!r}")
            return None

    def parse(self, tree) -> bool | None:
        if isinstance(tree, Exception):
            return None

        if tree is None:
            return False

        return tree.xpath(f"boolean(//fieldset[contains(., '{self.major}')])")

    def scrape(self, url: str) -> str | None:
        tree = self.fetch(url)
        has_target = self.parse(tree)
        if has_target is None:
            return None
        return url if has_target else ''

    def close(self):
        self.driver.quit()