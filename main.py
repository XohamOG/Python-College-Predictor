from college_logic.loadCsv import loadCsv
from college_logic.predict_college import predict_colleges
from MongoDb.fetching import connect_to_mongodb, fetch_score_and_gmail


# Establish MongoDB connection
db = connect_to_mongodb()

# Fetch Score and Gmail from MongoDB collection
collection_name = 'scores'
data = fetch_score_and_gmail(db, collection_name)

# Example: Print fetched data
for record in data:
    print(f"Score: {record['Score']}, Gmail: {record['Gmail']}")


#----------------------------------------------------------------------------------------------



#cutoff snippet 

# Path to your CSV file
csv_file_path = r'C:\Users\HP\Desktop\Python College Predictor\college_logic\Colleges.csv'

# Load the JEE cutoffs from the CSV file
cutoffs = loadCsv(csv_file_path)
connect_to_mongodb()
print('hello')
for student in fetch_score_and_gmail(db,collection_name):
    eligible_colleges = predict_colleges(cutoffs, student)
    
    if eligible_colleges:
        body = f"Dear {student['name']},\n\nBased on your  score and category, you are eligible for the following courses in the preferred colleges:\n"
        for college, courses in eligible_colleges.items():
            body += f"\n{college}:\n" + "\n".join(courses) + "\n"
    else:
        body = f"Dear {student['name']},\n\nUnfortunately, based on your  score and category, you are not eligible for any of your preferred courses in the listed colleges."
    
    print(f"Sending email to {student['email']}:\n{body}\n")
    # send_email(student['email'], " College Predictor Results", body)

