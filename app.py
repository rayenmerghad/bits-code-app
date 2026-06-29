import ddtrace.auto
from flask import Flask, jsonify, request
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
    3: {"id": 3, "name": "Widget C", "stock": 25,  "price": 49.99},
}

ORDERS = {
    1: {"product_id": 1, "qty": 2},
    2: {"product_id": 3, "qty": 1},
    3: {"product_id": 2, "qty": 5},
}


# N+1 QUERY PATTERN — fetches each product individually in a loop
# instead of loading all products in one batched call.
# Each call to get_product_by_id() simulates a separate DB round-trip.
# At scale: 100 orders = 100 sequential queries = O(n) latency.

def get_product_by_id(pid):
    time.sleep(0.10)   # simulates per-item DB lookup
    return PRODUCTS.get(pid)

@app.route("/orders/summary")
def orders_summary():
    result = []
    for order_id, order in ORDERS.items():
        product = get_product_by_id(order["product_id"])  # N+1 here
        if product:
            result.append({
                "order_id": order_id,
                "product":  product["name"],
                "qty":      order["qty"],
                "total":    round(product["price"] * order["qty"], 2),
            })
    return jsonify(result)


@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=8080, debug=True)