import time
from playwright.sync_api import Page, ElementHandle
from typing import List


def _with_retry(fn, retries: int = 2, delay: float = 1.0):
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(delay * (attempt + 1))
    raise last_exc


def click(page: Page, selector: str, timeout: int = 5000) -> None:
    page.wait_for_selector(selector, timeout=timeout)
    _with_retry(lambda: page.click(selector))


def fill(page: Page, selector: str, value: str, timeout: int = 5000) -> None:
    page.wait_for_selector(selector, timeout=timeout)
    _with_retry(lambda: page.fill(selector, value))


def get_text(page: Page, selector: str, timeout: int = 5000) -> str:
    page.wait_for_selector(selector, timeout=timeout)
    return _with_retry(lambda: page.inner_text(selector))


def get_all_elements(page: Page, selector: str, timeout: int = 5000) -> List[ElementHandle]:
    page.wait_for_selector(selector, timeout=timeout)
    return _with_retry(lambda: page.query_selector_all(selector))
