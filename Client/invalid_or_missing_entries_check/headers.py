# Check for bad headers
# Prab

import csv
import datetime

# checks for bad header formatting

def check_entries(filename):
    f = open(filename)
    filecsv = csv.reader(f)
    header = next(filecsv)
    rows = []
    for row in csvreader:
        rows.append(row)
    
    
# Example
if check_entries('MED_DATA_20220803153918.csv'):
    print("BAD ENTRY FOUND in MED_DATA_20220803153918.csv")
