from fetching import fetch_score_and_gmail
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient


collection_name = score



# Define Google Sheets and MongoDB connection settings
scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\HP\Desktop\CollegePredict\credentials.json', scope)
gc = gspread.authorize(credentials)

# Open a Google Sheets spreadsheet by its URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1uQ9T4JTO4N75pW4H2p0lgPpw_QeCik5ONx9sMdrfJao/edit?resourcekey=&gid=1385259069#gid=1385259069'
sh = gc.open_by_url(spreadsheet_url)
worksheet = sh.sheet1

# Get all values from the sheet
values = worksheet.get_all_values()

# Assuming the first row contains column headers
headers = values[0]
timestamp_index = headers.index('Timestamp') if 'Timestamp' in headers else None
name_index = headers.index('Name') if 'Name' in headers else None
gmail_index = headers.index('Gmail') if 'Gmail' in headers else None
score_index = headers.index('Score') if 'Score' in headers else None
category_index = headers.index('Category') if 'Category' in headers else None
preferred_courses_index = headers.index('Preferred Courses') if 'Preferred Courses' in headers else None

# Check if all required columns are found
if None in [timestamp_index, name_index, gmail_index, score_index, category_index, preferred_courses_index]:
    missing_columns = [header for header, index in zip(['Timestamp', 'Name', 'Gmail', 'Score', 'Category', 'Preferred Courses'], 
                                                       [timestamp_index, name_index, gmail_index, score_index, category_index, preferred_courses_index]) if index is None]
    raise ValueError(f"Missing columns in Google Sheet: {missing_columns}")

# Extract data for the required columns
data = []
for row in values[1:]:  # Skip the header row
    timestamp = row[timestamp_index]
    name = row[name_index]
    gmail = row[gmail_index]
    score = row[score_index]
    category = row[category_index]
    preferred_courses = row[preferred_courses_index]
    data.append({'Timestamp': timestamp, 'Name': name, 'Gmail': gmail, 'Score': score, 'Category': category, 'Preferred Courses': preferred_courses})

print("All records (Timestamp, Name, Gmail, Score, Category, Preferred Courses):")
for record in data:
    print(f"Timestamp: {record['Timestamp']}, Name: {record['Name']}, Gmail: {record['Gmail']}, Score: {record['Score']}, Category: {record['Category']}, Preferred Courses: {record['Preferred Courses']}")

# Function to establish MongoDB connection
def connect_to_mongodb(host='localhost', port=27017, db_name='mydatabase'):
    client = MongoClient(host, port)
    db = client[db_name]
    return db

# Function to fetch specific fields from MongoDB collection
def fetch_specific_fields(db, collection_name, fields):
    collection = db[collection_name]
    projection = {field: 1 for field in fields}
    projection['_id'] = 0  # Exclude the '_id' field
    return list(collection.find({}, projection))



fetch_score_and_gmail(db, collection_name)

# MongoDB connection settings
db = connect_to_mongodb()
collection_name = 'students'  # Replace 'students' with your collection name
collection = db[collection_name]

# Function to check if a document with the same Timestamp already exists in MongoDB
def document_exists(timestamp):
    return collection.find_one({'Timestamp': timestamp}) is not None

# Insert only new data into MongoDB
new_data_to_insert = []
for record in data:
    if not document_exists(record['Timestamp']):
        new_data_to_insert.append(record)

if new_data_to_insert:
    # Insert new data into MongoDB
    result = collection.insert_many(new_data_to_insert)
    print(f"Inserted {len(result.inserted_ids)} new documents into MongoDB.")
else:
    print("No new data to insert into MongoDB.")

# Fetch specific fields from MongoDB
fields_to_fetch = ['Timestamp', 'Name', 'Gmail', 'Score', 'Category', 'Preferred Courses']
fetched_data = fetch_specific_fields(db, collection_name, fields_to_fetch)

print("Fetched data from MongoDB:")
for record in fetched_data:
    print(record)
