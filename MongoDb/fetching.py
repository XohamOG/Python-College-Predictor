import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Function to establish MongoDB connection
def connect_to_mongodb(host='localhost', port=27017, db_name='mydatabase'):
    client = MongoClient(host, port)
    db = client[db_name]
    return db

# Connect to MongoDB
db = connect_to_mongodb()
collection_name = 'scores'
collection = db[collection_name]
last_processed_collection = 'last_processed'
last_processed_db = db[last_processed_collection]

# Function to fetch specific fields from MongoDB collection
def fetch_specific_fields(db, collection_name, fields, last_processed_id):
    collection = db[collection_name]
    projection = {field: 1 for field in fields}
    projection['_id'] = 1  #include imp***
    raw_data = list(collection.find({'_id': {'$gt': ObjectId(last_processed_id)}}, projection))
    
    # Convert fields to the correct types
    for record in raw_data:
        if 'Score' in record:
            record['Score'] = int(record['Score'])
        if 'Preferred Courses' in record:
            if isinstance(record['Preferred Courses'], str):
                record['Preferred Courses'] = record['Preferred Courses'].strip("[]").split(',')
                record['Preferred Courses'] = [course.strip() for course in record['Preferred Courses']]
    
    return raw_data

# Function to get the last processed record's ObjectId
def get_last_processed_id():
    record = last_processed_db.find_one()
    if record and 'last_processed_id' in record:
        return record['last_processed_id']
    else:
        return '000000000000000000000000'  # Default to the smallest ObjectId if no record found

# Function to update the last processed record's ObjectId
def update_last_processed_id(last_processed_id):
    last_processed_db.update_one({}, {'$set': {'last_processed_id': last_processed_id}}, upsert=True)

# Fetch specific fields from MongoDB
fields_to_fetch = ['Name', 'Gmail', 'Score', 'Category', 'Preferred Courses']
last_processed_id = get_last_processed_id()
fetched_data = fetch_specific_fields(db, collection_name, fields_to_fetch, last_processed_id)

print("Fetched data from MongoDB:")
for record in fetched_data:
    print(record)
