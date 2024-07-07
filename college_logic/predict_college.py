import csv
from college_logic.loadCsv import loadCsv

cutoffs = loadCsv(r"C:\Users\HP\Desktop\Python College Predictor\college_logic\Colleges.csv")


def predict_colleges(cutoffs, student):
    score = int(student['Score'])  # Convert score to an integer imp
    category = student['Category']
    preferred_courses = student['Preferred Courses']  # Convert preferred courses to a list imp
    
    eligible_colleges = {}

    for college, courses in cutoffs.items():
        for course, course_cutoffs in courses.items():
            if course in preferred_courses and score <= course_cutoffs.get(category, float('inf')):
                if college not in eligible_colleges:
                    eligible_colleges[college] = []
                eligible_colleges[college].append(course)
    
    return eligible_colleges




