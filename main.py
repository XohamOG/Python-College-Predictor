import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from college_logic.loadCsv import loadCsv
from college_logic.predict_college import predict_colleges
from MongoDb.fetching import connect_to_mongodb, fetch_specific_fields, get_last_processed_id, update_last_processed_id
import subprocess
import time
from bson.objectid import ObjectId
from password import password
#--------------------------------------------------------------------------------------------------------

# Email configuration
sender_email = 'patilsohamaruntestcode@gmail.com'  # Replace with your email address
sender_password = password  # Replace with your email password
smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server address
smtp_port = 587  # Replace with your SMTP server port

# MongoDB collection name for tracking sent emails
sent_emails_collection = 'sent_emails'
last_processed_collection = 'last_processed'

def send_email(receiver_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print(f"Email sent to {receiver_email}")
            return True  # Return True if email sent successfully
    except Exception as e:
        print(f"Failed to send email to {receiver_email}. Error: {str(e)}")
        return False  # Return False if email sending failed

#--------------------------------------------------------------------------------------------------------

# Establish MongoDB connection
db = connect_to_mongodb()
# Fetch Score and Gmail from MongoDB collection
collection_name = 'scores'

# MongoDB collection for tracking sent emails
sent_emails_db = db[sent_emails_collection]

# MongoDB collection for tracking the last processed record
last_processed_db = db[last_processed_collection]

#--------------------------------------------------------------------------------------------------------

# Path to your CSV file
csv_file_path = r'C:\Users\HP\Desktop\Python College Predictor\college_logic\Colleges.csv'

# Load the JEE cutoffs from the CSV file
cutoffs = loadCsv(csv_file_path)

#--------------------------------------------------------------------------------------------------------

# Main logic to fetch data and send emails
def main():
    while True:
        # running the googleforms.py in a main.py script independently 
        file_path = r'C:\Users\HP\Desktop\Python College Predictor\Google_Forms_logic\googleforms.py'
        subprocess.run(['python', file_path])

        last_processed_id = get_last_processed_id()
        fields_to_fetch = ['_id', 'Name', 'Gmail', 'Score', 'Category', 'Preferred Courses']
        fetched_data = fetch_specific_fields(db, collection_name, fields_to_fetch, last_processed_id)

        for student in fetched_data:
            eligible_colleges = predict_colleges(cutoffs, student)
            print(eligible_colleges)

            if eligible_colleges:   
                body = f"Dear {student['Name']},\n\nBased on your Rank and category, you are eligible for the following courses in the preferred colleges:\n"
                for college, preferred_courses in eligible_colleges.items():
                    body += f"\n{college}:\n" + "\n".join(preferred_courses) + "\n"
            else:
                body = f"Dear {student['Name']},\n\nUnfortunately, based on your score and category, you are not eligible for any of your preferred courses in the listed colleges."
            
            print(f"Sending email to {student['Gmail']}:\n{body}\n")

            # Attempt to send email
            if send_email(student['Gmail'], "College Predictor Results", body):
                update_last_processed_id(str(student['_id']))  # Update the last processed ObjectId
            else:
                print(f"Failed to send email to {student['Gmail']}.")


        time.sleep(3600) 

if __name__ == "__main__":
    main()
