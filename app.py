from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Widget A", "stock": 100, "price": 9.99},
    2: {"id": 2, "name": "Widget B", "stock": 0,   "price": 24.99},
}


@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))


# BUG: TypeError when "discount" query param is passed as a string
# and used directly in arithmetic without conversion.
@app.route("/products/<int:pid>/discounted-price")
def discounted_price(pid):
    p = PRODUCTS.get(pid)
    if not p:
        return jsonify({"error": "not found"}), 404

    discount = request.args.get("discount")  # comes in as a string, e.g. "5"
    final_price = p["price"] - discount       # TypeError: unsupported operand type(s) for -: 'float' and 'str'
    return jsonify({"final_price": final_price})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=8080, debug=True)