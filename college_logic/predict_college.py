

import csv

def loadCsv(csv_file_path):
    cutoffs = {}
    
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            college = row['College']
            course = row['Course']
            if college not in cutoffs:
                cutoffs[college] = {}
            if course not in cutoffs[college]:
                cutoffs[college][course] = {}
            cutoffs[college][course]['GOPEN'] = int(row['GOPEN'])
            cutoffs[college][course]['LOPEN'] = int(row['LOPEN'])
            cutoffs[college][course]['GOBC'] = int(row['GOBC'])
            cutoffs[college][course]['LOBC'] = int(row['LOBC'])
            cutoffs[college][course]['GSC'] = int(row['GSC'])
            cutoffs[college][course]['LSC'] = int(row['LSC'])
            cutoffs[college][course]['GST'] = int(row['GST'])
            cutoffs[college][course]['LST'] = int(row['LST'])
    
    return cutoffs



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




