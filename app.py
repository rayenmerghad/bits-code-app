import ddtrace.auto
from flask import Flask, jsonify, request
import time

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
}

# BUG 1: fixed
@app.route("/products/<int:pid>/score")
def score(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    stock = p["stock"]
    result = 100 if stock > 0 else 0
    return jsonify({"score": result})

# BUG 2: still wrong (kept intentionally)
@app.route("/products/<int:pid>/price")
def discounted_price(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    discount = float(request.args.get("discount", 0))
    final = p["price"] * (discount / 100)  # BUG: should be price * (1 - discount/100)
    return jsonify({"original": p["price"], "final": final})

# BUG 3: audit log grows forever in memory + slow sleep on every request
# Every call appends to a global list that is never cleared.
# Datadog APM will show latency spike + memory growth over time.
audit_log = []

@app.route("/products/<int:pid>/view")
def view_product(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404

    time.sleep(0.2)  # BUG: simulates slow "audit write" that should be async

    audit_log.append({          # BUG: unbounded list, never flushed
        "pid": pid,
        "ts": time.time(),
        "name": p["name"],
    })

    return jsonify({"product": p, "total_views": len(audit_log)})

@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)