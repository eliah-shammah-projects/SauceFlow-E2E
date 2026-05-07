# AI Bugs — Bugs Found and Fixed During Development

This document records bugs that were identified and corrected during the development of SauceFlow E2E, including how each was discovered and resolved.

---

## Bug 1 — Playwright browser closed prematurely by garbage collector

**File:** `automation/browser_manager.py`

**What happened:**
The Playwright server was shutting down before the browser finished its work. This caused intermittent failures during checkout with no clear error message.

**Root cause:**
Python's garbage collector was collecting the `playwright` object from memory while the browser was still open and in use. Once the object was collected, the Playwright server stopped — taking the browser with it.

**How it was found:**
During a systematic AI review requested before advancing to the next phase, Claude identified this as a potential instability in the browser lifecycle management.

**How it was fixed:**
A `_playwright_registry` dictionary was introduced in `browser_manager.py` to hold a reference to each active `playwright` instance, keyed by the browser's `id`. This prevents the GC from collecting the object while the browser is alive.

```python
_playwright_registry: dict = {}

def open_browser():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    _playwright_registry[id(browser)] = pw  # keeps pw alive
    return browser, page

def close_browser(browser):
    browser.close()
    pw = _playwright_registry.pop(id(browser), None)
    if pw:
        pw.stop()
```

**Process:** AI found the bug during review → proposed the fix → developer approved → applied.

---

## Bug 2 — SauceDemo has no native search

**Files:** `services/search_service.py`, `automation/selectors.py`

**What happened:**
The initial assumption was that SauceDemo had a search bar or filtering feature that the robot could interact with directly — type a product name and get filtered results.

**Root cause:**
SauceDemo is a static demo store. It displays all products on a single page with no search, filter, or pagination functionality.

**How it was found:**
Discovered during the planning phase when Claude mapped out the automation flow and inspected the SauceDemo structure. The expected search selector did not exist.

**How it was fixed:**
The approach was changed entirely: instead of searching on the site, the robot now collects **all products** from the page and filters them in Python by name (case-insensitive substring match) and maximum price.

```python
items = get_all_elements(page, sel.PRODUCT_LIST)
products = []
for item in items:
    title = item.query_selector(sel.PRODUCT_NAME).inner_text()
    price = float(item.query_selector(sel.PRODUCT_PRICE).inner_text().replace("$", ""))
    if name.lower() in title.lower() and price <= max_price:
        products.append(...)

return sorted(products, key=lambda p: p.price)
```

**Process:** AI identified the missing feature during planning → proposed collect-all-and-filter approach → developer approved → applied.
