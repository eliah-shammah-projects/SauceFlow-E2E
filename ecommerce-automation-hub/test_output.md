# Test Output

## All Tests — `tests/`

**Run date:** 2026-05-10  
**Python:** 3.14.2  
**pytest:** 9.0.3  

```
=================== test session starts ===================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\97258\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\97258\Desktop\SauceFlow E2E\ecommerce-automation-hub
collected 14 items

tests/test_e2e.py::test_full_flow_search_checkout_screenshot PASSED [  7%]
tests/test_unit.py::test_product_price_is_float PASSED [ 14%]
tests/test_unit.py::test_product_currency_is_usd PASSED [ 21%]
tests/test_unit.py::test_product_fields PASSED       [ 28%]
tests/test_unit.py::test_cart_add PASSED             [ 35%]
tests/test_unit.py::test_cart_remove PASSED          [ 42%]
tests/test_unit.py::test_cart_total PASSED           [ 50%]
tests/test_unit.py::test_cart_total_empty PASSED     [ 57%]
tests/test_unit.py::test_price_parse_strips_dollar PASSED [ 64%]
tests/test_unit.py::test_price_parse_two_decimal_places PASSED [ 71%]
tests/test_unit.py::test_filter_by_name PASSED       [ 78%]
tests/test_unit.py::test_filter_by_max_price PASSED  [ 85%]
tests/test_unit.py::test_cheapest_comes_first PASSED [ 92%]
tests/test_unit.py::test_filter_no_match_returns_empty PASSED [100%]

=================== 14 passed in 10.90s ===================
```

**Result: 14 passed, 0 failed**  
**Flow covered:** Search → Add to cart → Checkout → Success → Screenshot gerado
