import requests
from lxml import html

class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })

    def fetch(self, url: str):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            return html.fromstring(response.content)

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def parse(self, tree) -> list:
        items = tree.xpath('//fieldset')

        for item in items:
            if 'PSICOLOGIA' in item.text:
                return self.base_url
            
        return ''

    def scrape(self):
        tree = self.fetch(self.base_url)
        return self.parse(tree)