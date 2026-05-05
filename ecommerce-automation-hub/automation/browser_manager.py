from playwright.sync_api import sync_playwright, Browser, Page


def open_browser() -> tuple[Browser, Page]:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    return browser, page


def close_browser(browser: Browser) -> None:
    browser.close()
