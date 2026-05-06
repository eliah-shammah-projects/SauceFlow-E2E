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
# Job store  {requestId: {status, resultados, error}}
# Compartilhado entre threads — protegido por lock
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
# Recebe item + preco_max, dispara robô em background,
# retorna requestId imediatamente para o frontend ir à /loading
# ──────────────────────────────────────────────

@api.route("/run-search", methods=["POST"])
def run_search():
    data = request.get_json(silent=True) or {}

    item = (data.get("item") or "").strip()
    if not item:
        return jsonify({"error": "O campo 'item' é obrigatório."}), 400

    try:
        max_price = float(data.get("preco_max", -1))
        if max_price <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "'preco_max' deve ser um número positivo."}), 400

    request_id = str(uuid.uuid4())

    with _lock:
        _jobs[request_id] = {"status": "running", "resultados": None, "error": None}

    def _run():
        _log(request_id, "search_start", {"item": item, "max_price": max_price})
        start = time.time()
        try:
            products = search_products(item, max_price)
            resultados = [_product_to_dict(p) for p in products]
            with _lock:
                _jobs[request_id]["status"] = "done"
                _jobs[request_id]["resultados"] = resultados
            _log(request_id, "search_done", {
                "count": len(resultados),
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
# Polling da tela /loading — retorna estado atual do job
# ──────────────────────────────────────────────

@api.route("/status/<request_id>", methods=["GET"])
def status(request_id):
    with _lock:
        job = _jobs.get(request_id)
        if job is None:
            return jsonify({"error": "requestId não encontrado."}), 404
        snapshot = dict(job)  # copia dentro do lock — evita race condition

    return jsonify({
        "status": snapshot["status"],        # "running" | "done" | "error"
        "resultados": snapshot["resultados"],
        "error": snapshot["error"],
    })


# ──────────────────────────────────────────────
# POST /run-checkout
# Recebe requestId + produto escolhido, executa compra,
# retorna status + caminho do screenshot
# ──────────────────────────────────────────────

@api.route("/run-checkout", methods=["POST"])
def run_checkout():
    data = request.get_json(silent=True) or {}

    request_id = data.get("requestId", "").strip()
    produto_dict = data.get("produto")

    if not request_id or not produto_dict:
        return jsonify({"error": "'requestId' e 'produto' são obrigatórios."}), 400

    with _lock:
        job = _jobs.get(request_id)

    if job is None:
        return jsonify({"error": "requestId não encontrado."}), 404

    if job["status"] != "done":
        return jsonify({"error": "A busca ainda não foi concluída."}), 409

    try:
        product = _dict_to_product(produto_dict)
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Dados do produto inválidos."}), 400

    _log(request_id, "checkout_start", {"product": product.title, "price": product.price})
    start = time.time()
    order = purchase_product(product)
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
