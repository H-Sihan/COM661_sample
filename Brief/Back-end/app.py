from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo.errors

app = Flask(__name__)

# Allow CORS for specific origins
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/my_database"
mongo = PyMongo(app)
db = mongo.db


@app.route('/items', methods=['GET'])
def get_items():
    try:
        items = list(db.items.find())
        for item in items:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return jsonify(items), 200
    except pymongo.errors.PyMongoError as e:
        return jsonify({"error": f"Failed to fetch items: {str(e)}"}), 500


@app.route('/items', methods=['POST'])
def add_item():
    # Check if the request contains JSON
    if request.is_json:
        data = request.json  # Parse JSON data
    else:
        # Parse form-data (for x-www-form-urlencoded or form-data)
        data = {
            "name": request.form.get("name"),
            "quantity": int(request.form.get("quantity", 0)),  # Convert to int
            "value": int(request.form.get("value", 0))      
        }

    # Validate input data
    if not data or 'name' not in data or 'value' not in data or 'quantity' not in data:
        return jsonify({"error": "Invalid input, ensure 'name', 'value', and 'quantity' are provided."}), 400

    try:
        # Insert data into MongoDB
        item_id = db.items.insert_one(data).inserted_id
        return jsonify({"_id": str(item_id), "message": "Item added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add item: {str(e)}"}), 500
    
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    print(f"PUT request received for ID: {id}")

    # Check if JSON payload is sent
    if request.is_json:
        data = request.json
    else:
        return jsonify({"error": "Invalid request format"}), 400

    # Log the received data
    print(f"Received data: {data}")

    # Ensure '_id' is not included in the update
    if '_id' in data:
        data.pop('_id')

    if not data or 'name' not in data or 'quantity' not in data or 'value' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    try:
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ObjectId"}), 400

        result = db.items.update_one({"_id": ObjectId(id)}, {"$set": data})
        print(f"Update result: {result.raw_result}")

        if result.matched_count == 0:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        print(f"Error during update: {str(e)}")
        return jsonify({"error": f"Failed to update item: {str(e)}"}), 500

    
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid item ID"}), 400

        result = db.items.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item deleted successfully"}), 200
    except pymongo.errors.PyMongoError as e:
        return jsonify({"error": f"Failed to delete item: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)