import ddtrace.auto
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Setup in-memory SQLite (simulates a real DB)
def get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

DB = get_db()
DB.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
DB.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, product_id INTEGER, qty INTEGER)")
DB.executemany("INSERT INTO products VALUES (?,?,?)", [(1,"Widget A",9.99),(2,"Widget B",24.99),(3,"Widget C",49.99)])
DB.executemany("INSERT INTO orders VALUES (?,?,?)", [(1,1,2),(2,3,1),(3,2,5),(4,1,3)])
DB.commit()


# N+1 PATTERN: one SQL query per order instead of a single JOIN
@app.route("/orders/summary")
def orders_summary():
    orders = DB.execute("SELECT * FROM orders").fetchall()
    result = []
    for order in orders:
        # BUG: separate query fired for every single order
        product = DB.execute(
            "SELECT * FROM products WHERE id = ?", (order["product_id"],)
        ).fetchone()
        result.append({
            "order_id": order["id"],
            "product":  product["name"],
            "qty":      order["qty"],
            "total":    round(product["price"] * order["qty"], 2),
        })
    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=8080, debug=True)