from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
}

@app.route("/products/<int:pid>/score")
def score(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    max_stock = max((product["stock"] for product in PRODUCTS.values()), default=0)
    if max_stock <= 0:
        score_value = 0.0
    else:
        score_value = (p["stock"] / max_stock) * 100
    return jsonify({"score": score_value})


@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)