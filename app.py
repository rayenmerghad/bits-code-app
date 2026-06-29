import ddtrace.auto
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
}

# BUG 1: ZeroDivisionError when stock == 0
@app.route("/products/<int:pid>/score")
def score(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    stock = p["stock"]
    result = 100 if stock > 0 else 0
    return jsonify({"score": result})

# BUG 2: discount formula is wrong (multiplies instead of subtracts)
@app.route("/products/<int:pid>/price")
def discounted_price(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    discount = float(request.args.get("discount", 0))
    final = p["price"] * (discount / 100)  # should be price * (1 - discount/100)
    return jsonify({"original": p["price"], "final": final})

@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)