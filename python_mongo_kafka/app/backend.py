from flask import Flask, jsonify
from pymongo import MongoClient
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['shop_db']
users_collection = db['users']
items_collection = db['items']

# Kafka consumer setup
consumer = KafkaConsumer(
    'purchase_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

@app.route('/items', methods=['GET'])
def get_items():
    items = list(items_collection.find({}, {'_id': 0}))
    return jsonify(items), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify(users), 200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'userID': user_id}, {'_id': 0})
    return jsonify(user), 200

# @app.route('/deluser/<user_id>', methods=['POST'])
# def del_user(user_id):
#     user = users_collection.find_one_and_delete({'userID': user_id})

# @app.route('/adduser/<user_id>.<user_name>', methods=['POST'])
# def add_user(user_id, user_name):
#     user = users_collection.insert_one({'userID': user_id, 'userName': user_name, 'purchases': []})

def consume_messages():
    for message in consumer:
        data = message.value
        print(f"Consumed message: {data}")
        users_collection.update_one(
            {'userID': data['user_id']},
            {'$push': {'purchases': data['item_id']}},
            upsert=True
        )

if __name__ == '__main__':
    threading.Thread(target=consume_messages, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)