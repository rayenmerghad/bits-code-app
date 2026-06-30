from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    total = db.Column(db.Float)


@app.route("/seed")
def seed():
    db.create_all()
    for i in range(1, 21):
        c = Customer(name=f"Customer {i}")
        db.session.add(c)
        db.session.flush()
        for j in range(3):
            db.session.add(Order(customer_id=c.id, total=10.0 * (j + 1)))
    db.session.commit()
    return jsonify({"status": "seeded"})


# BUG: N+1 query pattern.
# This runs 1 query to get all customers, then loops and runs
# 1 additional query PER customer to fetch their orders = N+1 total queries.
@app.route("/customers/orders-summary")
def orders_summary_n_plus_1():
    customers = Customer.query.all()  # query #1
    result = []
    for c in customers:
        # separate query per customer -> N additional queries
        orders = Order.query.filter_by(customer_id=c.id).all()
        result.append({
            "customer": c.name,
            "order_count": len(orders),
            "total_spent": sum(o.total for o in orders),
        })
    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=8080, debug=True)