import os
from datetime import datetime
from domain.models import Product, Order
from automation.browser_manager import open_browser, close_browser
from automation.actions import click, fill, get_all_elements
import automation.selectors as sel


def purchase_product(product: Product) -> Order:
    browser, page = open_browser()
    screenshot_path = None
    try:
        page.goto("https://www.saucedemo.com")
        fill(page, sel.USERNAME_INPUT, os.getenv("SAUCE_USERNAME"))
        fill(page, sel.PASSWORD_INPUT, os.getenv("SAUCE_PASSWORD"))
        click(page, sel.LOGIN_BUTTON)

        items = get_all_elements(page, sel.PRODUCT_LIST)
        for item in items:
            title = item.query_selector(sel.PRODUCT_NAME).inner_text()
            if title == product.title:
                item.query_selector(sel.ADD_TO_CART_BUTTON).click()
                break

        click(page, sel.CART_ICON)
        click(page, sel.CHECKOUT_BUTTON)

        fill(page, sel.FIRST_NAME_INPUT, os.getenv("CHECKOUT_FIRST_NAME", "John"))
        fill(page, sel.LAST_NAME_INPUT, os.getenv("CHECKOUT_LAST_NAME", "Doe"))
        fill(page, sel.POSTAL_CODE_INPUT, os.getenv("CHECKOUT_POSTAL_CODE", "12345"))
        click(page, sel.CONTINUE_BUTTON)
        click(page, sel.FINISH_BUTTON)

        filename = f"confirmation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = f"static/screenshots/{filename}"
        page.screenshot(path=screenshot_path)

        return Order(
            items=[product],
            total=product.price,
            success=True,
            screenshot_path=screenshot_path
        )
    except Exception as e:
        return Order(
            items=[product],
            total=product.price,
            success=False,
            screenshot_path=screenshot_path,
            error=str(e)
        )
    finally:
        close_browser(browser)
