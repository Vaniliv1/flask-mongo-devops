from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["devops"]
messages = db["messages"]

@app.route('/message', methods=['POST'])
def add_message():
    data = request.json
    if "text" in data:
        messages.insert_one({"text": data["text"]})
        return jsonify({"status": "Message added"}), 201
    return jsonify({"error": "Text required"}), 400

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify([msg["text"] for msg in messages.find()]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))