import logging
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
}

@app.route("/products/<int:pid>/score")
def score(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404

    try:
        # BUG (intentionally left in): ZeroDivisionError when stock == 0
        score_value = (p["stock"] / p["stock"]) * 100
    except ZeroDivisionError:
        # APM hook: log a structured, greppable error an automation
        # pipeline can match on and then apply the remediation below.
        logger.error(
            "ZeroDivisionError in /products/%s/score | stock=%s",
            pid, p["stock"],
            extra={"error_code": "SCORE_DIV_ZERO", "product_id": pid},
        )
        # Remediation: treat zero stock as score 0 instead of crashing.
        score_value = 0

    return jsonify({"score": score_value})

@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)