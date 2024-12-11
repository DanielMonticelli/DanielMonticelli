from playwright.sync_api import sync_playwright
from classes import Path


class RPA:

    def __init__(self):
        self.paths = Path()
        self.price_list = []

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=False) # Remover "headless=False" caso queira executar sem interface
            page = browser.new_page()

            page.goto(self.paths.web_link)
            page.wait_for_load_state("domcontentloaded")
            prices = page.query_selector_all(self.paths.prices)

            for p in prices:
                self.price_list.append(p.text_content())

            page.close()
            browser.close()

        return self.price_list
