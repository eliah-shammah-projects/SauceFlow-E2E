import os
import pytest
from services.search_service import search_products
from services.purchase_service import purchase_product


def test_full_flow_search_checkout_screenshot(credentials):
    # 1. Search
    products = search_products("sauce", 50.0)
    assert len(products) > 0, "Nenhum produto encontrado para 'sauce' abaixo de $50"

    # 2. Cheapest first (already sorted)
    product = products[0]
    assert isinstance(product.price, float)
    assert product.currency == "USD"

    # 3. Checkout
    order = purchase_product(product)

    # 4. Success
    assert order.success is True, f"Checkout falhou: {order.error}"

    # 5. Screenshot obrigatório
    assert order.screenshot_path is not None, "Screenshot não foi gerado"
    abs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        order.screenshot_path.replace("/", os.sep)
    )
    assert os.path.isfile(abs_path), f"Arquivo de screenshot não encontrado: {abs_path}"
