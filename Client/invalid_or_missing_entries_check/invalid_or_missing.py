# Check for missing or invalid(bad) entries
# Prab

import csv

def check_missing(filename):
    # get rows
    f = open(filename)
    filecsv = csv.reader(f)
    rows = []
    for row in filecsv:
        rows.append(row)
    # check for any empty values
    for x in rows:
        for y in x:
            if y == '':
                return True
    return False

def check_bad(filename):
    # get rows
    f = open(filename)
    filecsv = csv.reader(f)
    rows = []
    for row in filecsv:
        rows.append(row)
    # remove header row
    rows.pop(0)
    # remove batch ID and timestamp from each row
    for row in rows:
        row.pop(0)
        row.pop(0)
    # check all values, if they can be converted from str to float
    for x in rows:
        for y in x:
            try:
                float(y)
            except:
                return True
    return False
                
                
    
# Example
if check_missing('MED_DATA_20220803153918.csv'):
    print("MISSING ENTRY FOUND in MED_DATA_20220803153918.csv")

if check_bad('MED_DATA_20220803153918.csv'):
    print("INVALD(BAD)ENTRY FOUND in MED_DATA_20220803153918.csv")
