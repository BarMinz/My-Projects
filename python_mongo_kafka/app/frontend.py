from flask import Flask, request, jsonify, render_template
from kafka import KafkaProducer
import requests
import json

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

API_SERVER_URL = 'http://localhost:5000'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buy', methods=['POST'])
def buy_item():
    data = request.json
    producer.send('purchase_topic', value=data)
    return jsonify({'status': 'success'}), 200

@app.route('/items', methods=['GET'])
def get_items():
    response = requests.get(f'{API_SERVER_URL}/items')
    return jsonify(response.json()), 200

@app.route('/users', methods=['GET'])
def get_users():
    response = requests.get(f'{API_SERVER_URL}/users')
    return jsonify(response.json()), 200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    response = requests.get(f'{API_SERVER_URL}/user/{user_id}')
    return jsonify(response.json()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)