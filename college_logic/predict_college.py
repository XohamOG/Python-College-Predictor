def predict_colleges(cutoffs, student):
    score = student['score']
    category = student['category']
    preferred_courses = student['preferred_courses']
    
    eligible_colleges = {}

    for college, courses in cutoffs.items():
        for course, course_cutoffs in courses.items():
            if course in preferred_courses and score <= course_cutoffs.get(category, float('inf')):
                if college not in eligible_colleges:
                    eligible_colleges[college] = []
                eligible_colleges[college].append(course)

    return eligible_colleges