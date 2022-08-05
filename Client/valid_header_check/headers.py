# Check for bad headers
# Prab

import csv
import datetime

# checks for bad header formatting

def check_header(filename):
    f = open(filename)
    filecsv = csv.reader(f)
    header = next(filecsv)
    valid_header = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6', 'reading7', 'reading8', 'reading9', 'reading10']
    if header != valid_header:
        return True
    else:
        return False
    
    
# Example
if check_header('MED_DATA_20220803153918.csv'):
    print("BAD HEADER FOUND in MED_DATA_20220803153918.csv")
