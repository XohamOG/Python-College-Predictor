from pymongo import MongoClient

# Function to establish MongoDB connection
def connect_to_mongodb(host='localhost', port=27017, db_name='mydatabase'):
    client = MongoClient(host, port)
    db = client[db_name]
    return db

# Function to fetch data from MongoDB collection
def fetch_data_from_collection(db, collection_name):
    collection = db[collection_name]
    return list(collection.find())  # Retrieve all documents as a list
