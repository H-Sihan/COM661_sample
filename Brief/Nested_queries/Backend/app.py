from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce_db"
mongo = PyMongo(app)

# Test Endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API connected to MongoDB!"})

# Get all products in the inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():
    store = mongo.db.stores.find_one({}, {"store.inventory": 1, "_id": 0})
    if store and "store" in store:
        return jsonify(store["store"].get("inventory", []))
    return jsonify({"error": "No inventory found"}), 404

# Search product by productId
@app.route("/inventory/<string:product_id>", methods=["GET"])
def get_product(product_id):
    store = mongo.db.stores.find_one({"store.inventory.productId": product_id},
                                      {"store.inventory.$": 1, "_id": 0})
    if store:
        return jsonify(store)
    return jsonify({"error": "Product not found"}), 404

# Add a review to a product
@app.route("/inventory/<string:product_id>/add_review", methods=["POST"])
def add_review(product_id):
    review = request.json
    result = mongo.db.stores.update_one(
        {"store.inventory.productId": product_id},
        {"$push": {"store.inventory.$.reviews": review}}
    )
    if result.modified_count > 0:
        return jsonify({"message": "Review added successfully"})
    return jsonify({"error": "Failed to add review"}), 400

# Get all orders
@app.route("/orders", methods=["GET"])
def get_orders():
    store = mongo.db.stores.find_one({}, {"store.orders": 1, "_id": 0})
    if store and "store" in store:
        return jsonify({"orders": store["store"].get("orders", [])})
    return jsonify({"error": "No orders found"}), 404

# Add a new order
@app.route("/orders", methods=["POST"])
def add_order():
    new_order = request.json
    result = mongo.db.stores.update_one(
        {}, {"$push": {"store.orders": new_order}}
    )
    if result.modified_count > 0:
        return jsonify({"message": "Order added successfully"})
    return jsonify({"error": "Failed to add order"}), 400

# Get orders by customerId
@app.route("/orders/<string:customer_id>", methods=["GET"])
def get_orders_by_customer(customer_id):
    store = mongo.db.stores.find_one(
        {"store.orders": {"$elemMatch": {"customerId": customer_id}}},
        {"store.orders": 1, "_id": 0}
    )
    if store and "store" in store:
        # Filter only orders matching the customer ID
        orders = [order for order in store["store"]["orders"] if order["customerId"] == customer_id]
        return jsonify({"orders": orders})
    return jsonify({"error": "No orders found for this customer"}), 404

if __name__ == "__main__":
    app.run(debug=True)