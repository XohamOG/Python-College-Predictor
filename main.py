from connection import connect_to_mongodb, fetch_score_and_gmail


# Establish MongoDB connection
db = connect_to_mongodb()

# Fetch Score and Gmail from MongoDB collection
collection_name = 'scores'
data = fetch_score_and_gmail(db, collection_name)

# Example: Print fetched data
for record in data:
    print(f"Score: {record['Score']}, Gmail: {record['Gmail']}")


print('hello')

