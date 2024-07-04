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
            cutoffs[college][course]['General'] = int(row['General'])
            cutoffs[college][course]['OBC'] = int(row['OBC'])
            cutoffs[college][course]['SC'] = int(row['SC'])
            cutoffs[college][course]['ST'] = int(row['ST'])
    
    return cutoffs


