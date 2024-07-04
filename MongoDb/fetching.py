import pymongo

from pymongo import MongoClient

# Function to establish MongoDB connection
def connect_to_mongodb(host='localhost', port=27017, db_name='mydatabase'):
    client = MongoClient(host, port)
    db = client[db_name]
    return db

# Function to fetch Score and Gmail from MongoDB collection
def fetch_score_and_gmail(db, collection_name):
    collection = db[collection_name]
    projection = {'Score': 1, 'Gmail': 1,'Category': 1,'Preffered_Courses':1,'_id': 0}  # Specify fields to retrieve
    return list(collection.find({}, projection))
