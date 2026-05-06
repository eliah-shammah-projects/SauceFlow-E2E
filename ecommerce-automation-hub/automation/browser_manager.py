from playwright.sync_api import sync_playwright, Browser, Page

# Guarda o playwright de cada browser aberto para garantir que não seja
# coletado pelo GC antes de fechar — sem isso o servidor Playwright encerra cedo
_playwright_registry: dict = {}


def open_browser() -> tuple[Browser, Page]:
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    _playwright_registry[id(browser)] = pw
    return browser, page


def close_browser(browser: Browser) -> None:
    browser.close()
    pw = _playwright_registry.pop(id(browser), None)
    if pw:
        pw.stop()
