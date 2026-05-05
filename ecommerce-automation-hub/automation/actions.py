from playwright.sync_api import Page, ElementHandle
from typing import List


def click(page: Page, selector: str, timeout: int = 5000) -> None:
    page.wait_for_selector(selector, timeout=timeout)
    page.click(selector)


def fill(page: Page, selector: str, value: str, timeout: int = 5000) -> None:
    page.wait_for_selector(selector, timeout=timeout)
    page.fill(selector, value)


def get_text(page: Page, selector: str, timeout: int = 5000) -> str:
    page.wait_for_selector(selector, timeout=timeout)
    return page.inner_text(selector)


def get_all_elements(page: Page, selector: str, timeout: int = 5000) -> List[ElementHandle]:
    page.wait_for_selector(selector, timeout=timeout)
    return page.query_selector_all(selector)
