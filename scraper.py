from playwright.sync_api import sync_playwright

class QuizScraper:

    def __init__(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=True)

    def fetch_page_content(self, url):
        page = self.browser.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        html = page.content()

        page.close()
        return html

    def close(self):
        try:
            if self.browser:
                self.browser.close()
        except:
            pass

        try:
            if self.pw:
                self.pw.stop()
        except:
            pass
