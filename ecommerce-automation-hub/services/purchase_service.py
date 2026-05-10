import os
from datetime import datetime
from domain.models import Product, Order
from automation.browser_manager import open_browser, close_browser
from automation.actions import click, fill, get_all_elements
import automation.selectors as sel

_SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static", "screenshots"
)


def purchase_product(product: Product, first_name: str, last_name: str, postal_code: str) -> Order:
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

        fill(page, sel.FIRST_NAME_INPUT, first_name)
        fill(page, sel.LAST_NAME_INPUT, last_name)
        fill(page, sel.POSTAL_CODE_INPUT, postal_code)
        click(page, sel.CONTINUE_BUTTON)
        click(page, sel.FINISH_BUTTON)

        filename = f"confirmation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        abs_path = os.path.join(_SCREENSHOTS_DIR, filename)
        page.screenshot(path=abs_path)
        screenshot_path = f"static/screenshots/{filename}"

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
