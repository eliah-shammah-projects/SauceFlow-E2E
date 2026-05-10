import json
import logging
import sys
from datetime import datetime, timezone
from flask import Flask, render_template
from dotenv import load_dotenv
from api.routes import api

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api)


class _JsonFormatter(logging.Formatter):
    def format(self, record):
        try:
            ts = datetime.now(timezone.utc).isoformat()
            msg = record.getMessage()
            try:
                payload = json.loads(msg)
                if isinstance(payload, dict):
                    payload.setdefault("ts", ts)
                    payload.setdefault("level", record.levelname)
                    payload.setdefault("logger", record.name)
                    return json.dumps(payload, ensure_ascii=False)
            except (json.JSONDecodeError, ValueError):
                pass
            return json.dumps({
                "ts": ts,
                "level": record.levelname,
                "logger": record.name,
                "msg": msg,
            }, ensure_ascii=False)
        except Exception:
            return super().format(record)


def _setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JsonFormatter())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loading")
def loading():
    return render_template("loading.html")


@app.route("/resultados")
def resultados():
    return render_template("resultados.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/checkout-status")
def checkout_status():
    return render_template("checkout.html")


if __name__ == "__main__":
    _setup_logging()
    app.run(debug=False, threaded=True, port=5002)
