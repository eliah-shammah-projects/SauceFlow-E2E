import pytest
from domain.models import Product, Cart, Order


# --- helpers ---

def make_product(title="Sauce Labs Backpack", price=29.99, pid=None):
    return Product(
        id=pid or title.lower().replace(" ", "-"),
        title=title,
        price=price,
        currency="USD",
        url="https://www.saucedemo.com",
        source="saucedemo",
    )


# --- Product ---

def test_product_price_is_float():
    p = make_product(price=9.99)
    assert isinstance(p.price, float)


def test_product_currency_is_usd():
    p = make_product()
    assert p.currency == "USD"


def test_product_fields():
    p = make_product(title="Bike Light", price=9.99, pid="bike-light")
    assert p.id == "bike-light"
    assert p.title == "Bike Light"
    assert p.source == "saucedemo"


# --- Cart ---

def test_cart_add():
    cart = Cart()
    cart.add(make_product())
    assert len(cart.items) == 1


def test_cart_remove():
    cart = Cart()
    p = make_product(pid="target")
    cart.add(p)
    cart.add(make_product(pid="other"))
    cart.remove("target")
    assert len(cart.items) == 1
    assert cart.items[0].id == "other"


def test_cart_total():
    cart = Cart()
    cart.add(make_product(price=10.00))
    cart.add(make_product(price=5.50))
    assert cart.total == pytest.approx(15.50)


def test_cart_total_empty():
    assert Cart().total == 0.0


# --- Price normalisation (lógica do search_service) ---

def test_price_parse_strips_dollar():
    raw = "$9.99"
    price = float(raw.replace("$", ""))
    assert price == pytest.approx(9.99)
    assert isinstance(price, float)


def test_price_parse_two_decimal_places():
    raw = "$29.99"
    price = float(raw.replace("$", ""))
    assert price == pytest.approx(29.99)


# --- Filtro / política de seleção (lógica do search_service) ---

def _filter(products, name, max_price):
    return sorted(
        [p for p in products if name.lower() in p.title.lower() and p.price <= max_price],
        key=lambda p: p.price,
    )


def test_filter_by_name():
    products = [
        make_product("Sauce Labs Backpack", 29.99),
        make_product("Sauce Labs Bike Light", 9.99),
        make_product("Sauce Labs Bolt T-Shirt", 15.99),
    ]
    result = _filter(products, "bike", 50.00)
    assert len(result) == 1
    assert result[0].title == "Sauce Labs Bike Light"


def test_filter_by_max_price():
    products = [
        make_product("Backpack", 29.99),
        make_product("Bike Light", 9.99),
    ]
    result = _filter(products, "a", 15.00)
    assert all(p.price <= 15.00 for p in result)


def test_cheapest_comes_first():
    products = [
        make_product("Backpack", 29.99),
        make_product("Bike Light", 9.99),
        make_product("T-Shirt", 15.99),
    ]
    result = _filter(products, "a", 50.00)
    prices = [p.price for p in result]
    assert prices == sorted(prices)


def test_filter_no_match_returns_empty():
    products = [make_product("Backpack", 29.99)]
    result = _filter(products, "nonexistent", 50.00)
    assert result == []
