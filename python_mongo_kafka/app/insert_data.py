from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['shop_db']

# Insert Users
users = [
    {
        "userID": "1",
        "userName": "Bar",
        "purchases": ["1", "2", "6"]
    },
    {
        "userID": "2",
        "userName": "Avihai",
        "purchases": ["1", "4", "6"]
    },
    {
        "userID": "3",
        "userName": "Slavik",
        "purchases": ["1", "5"]
    },
    {
        "userID": "4",
        "userName": "Evgeny",
        "purchases": ["3", "5"]
    },
    {
        "userID": "5",
        "userName": "Vova",
        "purchases": ["2", "6"]
    }
]

db.users.insert_many(users)

# Insert Items
items = [
    {
        "id": "1",
        "name": "Xbox",
        "price": 299.99
    },
    {
        "id": "2",
        "name": "PlayStation",
        "price": 499.99
    },
    {
        "id": "3",
        "name": "PC",
        "price": 999.99
    },
    {
        "id": "4",
        "name": "Camera",
        "price": 199.99
    },
    {
        "id": "5",
        "name": "Headphones",
        "price": 89.99
    },
    {
        "id": "6",
        "name": "Smartphone",
        "price": 799.99
    }
]

db.items.insert_many(items)

print("Data inserted successfully!")