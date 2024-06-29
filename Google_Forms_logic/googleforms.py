import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient

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
name_index = headers.index('Name') if 'Name' in headers else None
score_index = headers.index('Marks') if 'Marks' in headers else None
gmail_index = headers.index('Gmail') if 'Gmail' in headers else None

# Check if all required columns are found
if None in [name_index, score_index, gmail_index]:
    missing_columns = [header for header, index in zip(['Name', 'Marks', 'Gmail'], [name_index, score_index, gmail_index]) if index is None]
    raise ValueError(f"Missing columns in Google Sheet: {missing_columns}")

# Extract data for 'Name', 'Score', and 'Gmail' columns
data = []
for row in values[1:]:  # Skip the header row
    name = row[name_index]
    score = row[score_index]
    gmail = row[gmail_index]
    data.append({'Name': name, 'Score': score, 'Gmail': gmail})

print("All records (Name, Score, Gmail):")
for record in data:
    print(f"Name: {record['Name']}, Score: {record['Score']}, Gmail: {record['Gmail']}")

# MongoDB connection settings
mongo_client = MongoClient('localhost', 27017)  # Assuming MongoDB is running locally
db = mongo_client['mydatabase']  # Replace 'mydatabase' with your database name
collection = db['scores']  # Replace 'scores' with your collection name

# Function to check if a document with the same Gmail already exists in MongoDB
def document_exists(gmail):
    return collection.find_one({'Gmail': gmail}) is not None

# Insert only new data into MongoDB
new_data_to_insert = []
for record in data:
    if not document_exists(record['Gmail']):
        new_data_to_insert.append(record)

if new_data_to_insert:
    # Insert new data into MongoDB
    result = collection.insert_many(new_data_to_insert)
    print(f"Inserted {len(result.inserted_ids)} new documents into MongoDB.")
else:
    print("No new data to insert into MongoDB.")


    


