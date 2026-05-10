import json
import logging
import time
import uuid
from threading import Lock, Thread

from flask import Blueprint, jsonify, request

from domain.models import Product
from services.purchase_service import purchase_product
from services.search_service import search_products

api = Blueprint("api", __name__)

# ──────────────────────────────────────────────
# Job store  {requestId: {status, results, error}}
# Shared between threads — protected by lock
# ──────────────────────────────────────────────
_jobs: dict = {}
_lock = Lock()

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _log(request_id: str, step: str, extra: dict) -> None:
    payload = {"requestId": request_id, "step": step, **extra}
    logger.info(json.dumps(payload, ensure_ascii=False))


def _product_to_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "title": p.title,
        "price": p.price,
        "currency": p.currency,
        "url": p.url,
        "source": p.source,
    }


def _dict_to_product(d: dict) -> Product:
    return Product(
        id=d["id"],
        title=d["title"],
        price=float(d["price"]),
        currency=d["currency"],
        url=d["url"],
        source=d["source"],
    )


# ──────────────────────────────────────────────
# POST /run-search
# Receives item + max_price, launches robot in background,
# returns requestId immediately so the frontend navigates to /loading
# ──────────────────────────────────────────────

@api.route("/run-search", methods=["POST"])
def run_search():
    data = request.get_json(silent=True) or {}

    item = (data.get("item") or "").strip()
    if not item:
        return jsonify({"error": "The 'item' field is required."}), 400

    try:
        max_price = float(data.get("max_price", -1))
        if max_price <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "'max_price' must be a positive number."}), 400

    request_id = str(uuid.uuid4())

    with _lock:
        _jobs[request_id] = {"status": "running", "results": None, "error": None}

    def _run():
        _log(request_id, "search_start", {"item": item, "max_price": max_price})
        start = time.time()
        try:
            products = search_products(item, max_price)
            results = [_product_to_dict(p) for p in products]
            with _lock:
                _jobs[request_id]["status"] = "done"
                _jobs[request_id]["results"] = results
            _log(request_id, "search_done", {
                "count": len(results),
                "duration_seconds": round(time.time() - start, 2),
            })
        except Exception as exc:
            with _lock:
                _jobs[request_id]["status"] = "error"
                _jobs[request_id]["error"] = str(exc)
            _log(request_id, "search_error", {
                "error": str(exc),
                "duration_seconds": round(time.time() - start, 2),
            })

    Thread(target=_run, daemon=True).start()
    return jsonify({"requestId": request_id}), 202


# ──────────────────────────────────────────────
# GET /status/<request_id>
# Polling from /loading — returns current job state
# ──────────────────────────────────────────────

@api.route("/status/<request_id>", methods=["GET"])
def status(request_id):
    with _lock:
        job = _jobs.get(request_id)
        if job is None:
            return jsonify({"error": "requestId not found."}), 404
        snapshot = dict(job)

    return jsonify({
        "status": snapshot["status"],
        "results": snapshot["results"],
        "error": snapshot["error"],
    })


# ──────────────────────────────────────────────
# POST /run-checkout
# Receives requestId + chosen product, executes purchase,
# returns status + screenshot path
# ──────────────────────────────────────────────

@api.route("/run-checkout", methods=["POST"])
def run_checkout():
    data = request.get_json(silent=True) or {}

    request_id = data.get("requestId", "").strip()
    product_dict = data.get("product")
    first_name = (data.get("firstName") or "").strip()
    last_name = (data.get("lastName") or "").strip()
    postal_code = (data.get("postalCode") or "").strip()

    if not request_id or not product_dict:
        return jsonify({"error": "'requestId' and 'product' are required."}), 400

    if not first_name or not last_name or not postal_code:
        return jsonify({"error": "Shipping details are required."}), 400

    with _lock:
        job = _jobs.get(request_id)

    if job is None:
        return jsonify({"error": "requestId not found."}), 404

    if job["status"] != "done":
        return jsonify({"error": "Search not completed yet."}), 409

    try:
        product = _dict_to_product(product_dict)
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid product data."}), 400

    _log(request_id, "checkout_start", {"product": product.title, "price": product.price})
    start = time.time()
    order = purchase_product(product, first_name, last_name, postal_code)
    duration = round(time.time() - start, 2)

    if order.success:
        _log(request_id, "checkout_done", {"total": order.total, "duration_seconds": duration})
        return jsonify({
            "status": "success",
            "total": order.total,
            "screenshot_path": order.screenshot_path,
        })

    _log(request_id, "checkout_error", {"error": order.error, "duration_seconds": duration})
    return jsonify({"status": "error", "error": order.error}), 500
