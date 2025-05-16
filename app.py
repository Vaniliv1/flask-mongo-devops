from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["devops"]
    messages = db["messages"]
except Exception as e:
    app.logger.error(f"MongoDB connection failed: {e}")
    messages = None

@app.route('/message', methods=['POST'])
def add_message():
    if not messages:
        return jsonify({"error": "Database unavailable"}), 500
    data = request.json
    if "text" in data:
        messages.insert_one({"text": data["text"]})
        return jsonify({"status": "Message successfully added"}), 201
    return jsonify({"error": "Text required"}), 400

@app.route('/messages', methods=['GET'])
def get_messages():
    if not messages:
        return jsonify({"error": "Database unavailable"}), 500
    return jsonify([msg["text"] for msg in messages.find()]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))