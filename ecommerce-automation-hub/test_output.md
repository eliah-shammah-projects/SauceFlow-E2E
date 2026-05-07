# Test Output

## Unit Tests — `tests/test_unit.py`

**Run date:** 2026-05-07  
**Python:** 3.14.2  
**pytest:** 9.0.3  

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: ecommerce-automation-hub
collecting ... collected 13 items

tests/test_unit.py::test_product_price_is_float PASSED                   [  7%]
tests/test_unit.py::test_product_currency_is_usd PASSED                  [ 15%]
tests/test_unit.py::test_product_fields PASSED                           [ 23%]
tests/test_unit.py::test_cart_add PASSED                                 [ 30%]
tests/test_unit.py::test_cart_remove PASSED                              [ 38%]
tests/test_unit.py::test_cart_total PASSED                               [ 46%]
tests/test_unit.py::test_cart_total_empty PASSED                         [ 53%]
tests/test_unit.py::test_price_parse_strips_dollar PASSED                [ 61%]
tests/test_unit.py::test_price_parse_two_decimal_places PASSED           [ 69%]
tests/test_unit.py::test_filter_by_name PASSED                           [ 76%]
tests/test_unit.py::test_filter_by_max_price PASSED                      [ 84%]
tests/test_unit.py::test_cheapest_comes_first PASSED                     [ 92%]
tests/test_unit.py::test_filter_no_match_returns_empty PASSED            [100%]

============================= 13 passed in 0.06s ==============================
```

**Result: 13 passed, 0 failed**

---

## E2E Tests — `tests/test_e2e.py`

**Run date:** 2026-05-07  
**Python:** 3.14.2  
**pytest:** 9.0.3  

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: ecommerce-automation-hub
collecting ... collected 1 item

tests/test_e2e.py::test_full_flow_search_checkout_screenshot PASSED      [100%]

============================= 1 passed in 13.82s ==============================
```

**Result: 1 passed, 0 failed**  
**Flow covered:** Search → Add to cart → Checkout → Success → Screenshot gerado
