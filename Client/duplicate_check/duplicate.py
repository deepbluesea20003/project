# Check for duplicate batch ids
# Prab

import csv
import datetime

# Function compares two files, returns True if duplicate found, False if not
def check_dup(file1, file2):
    f = open(file1)
    g = open(file2)
    file1csv = csv.reader(f)
    file2csv = csv.reader(g)
    file1rows = []
    file2rows = []
    for entry in file1csv:
        file1rows.append(entry[0])
    for entry in file2csv:
        file2rows.append(entry[0])
    del file1rows[0]
    del file1rows[1]
    result = [v for v in file1rows if v in file2rows]
    if result:
        return True
    else:
        return False
    f.close()
    g.close()
    
    
# Example
if check_dup('MED_DATA_20220803153918.csv', 'MED_DATA_20220803153920.csv'):
    print("DUPLICATE BATCH IDs FOUND")
    f = open('log.txt','a+')
    error_msg = str(datetime.datetime.now()) + ': ERROR DUPLICATE:MED_DATA_20220803153918.CSV AND MED_DATA_20220803153920.CSV HAVE DUPLICATE BATCH IDs\n'
    f.write(error_msg)
    f.close()
