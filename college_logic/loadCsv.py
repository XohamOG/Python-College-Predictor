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


