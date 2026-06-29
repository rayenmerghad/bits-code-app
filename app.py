from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
}

# BUG: crashes with ZeroDivisionError when stock == 0
@app.route("/products/<int:pid>/score")
def score(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404
    score = (p["stock"] / p["stock"]) * 100  # ZeroDivisionError when stock=0
    return jsonify({"score": score})


@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)