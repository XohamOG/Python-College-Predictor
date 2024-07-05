import csv

def loadCsv(csv_file_path):
    cutoffs = {}
    
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            college = row['College']
            courses = row['Course']
            if college not in cutoffs:
                cutoffs[college] = {}
            if courses not in cutoffs[college]:
                cutoffs[college][courses] = {}
            cutoffs[college][courses]['GOPEN'] = int(row['GOPEN'])
            cutoffs[college][courses]['LOPEN'] = int(row['LOPEN'])
            cutoffs[college][courses]['GOBC'] = int(row['GOBC'])
            cutoffs[college][courses]['LOBC'] = int(row['LOBC'])
            cutoffs[college][courses]['GSC'] = int(row['GSC'])
            cutoffs[college][courses]['LSC'] = int(row['LSC'])
            cutoffs[college][courses]['GST'] = int(row['GST'])
            cutoffs[college][courses]['LST'] = int(row['LST'])
    
    return cutoffs


