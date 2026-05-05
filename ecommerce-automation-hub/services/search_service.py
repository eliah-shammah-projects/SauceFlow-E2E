import os
from typing import List
from domain.models import Product
from automation.browser_manager import open_browser, close_browser
from automation.actions import click, fill, get_all_elements
import automation.selectors as sel


def search_products(name: str, max_price: float) -> List[Product]:
    browser, page = open_browser()
    try:
        page.goto("https://www.saucedemo.com")
        fill(page, sel.USERNAME_INPUT, os.getenv("SAUCE_USERNAME"))
        fill(page, sel.PASSWORD_INPUT, os.getenv("SAUCE_PASSWORD"))
        click(page, sel.LOGIN_BUTTON)

        items = get_all_elements(page, sel.PRODUCT_LIST)

        products = []
        for item in items:
            title = item.query_selector(sel.PRODUCT_NAME).inner_text()
            price_text = item.query_selector(sel.PRODUCT_PRICE).inner_text()
            price = float(price_text.replace("$", ""))

            if name.lower() in title.lower() and price <= max_price:
                products.append(Product(
                    id=title.lower().replace(" ", "-"),
                    title=title,
                    price=price,
                    currency="USD",
                    url="https://www.saucedemo.com",
                    source="saucedemo"
                ))

        return sorted(products, key=lambda p: p.price)
    finally:
        close_browser(browser)
