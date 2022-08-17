#purpose: chech for missing columns on a row
#author: Ella

#MED_DATA_20210701153942 has missing column on row to test against

import csv

def check_missing(filename):
    valid_file = True
    with open(filename) as med_file:
        csv_reader = csv.DictReader(med_file)
        #each 'row' is a dictionary linking the header and correpsonding value for that row
        for row in csv_reader:
            #iterates over each value to check if it's nil
            for value in row.values():
                if value == None:
                    valid_file = False
    return valid_file
                    
                

#tests
print(check_missing("MED_DATA_20210701153942.csv")) #returns false yay
print(check_missing("MED_DATA_20210701153947.csv")) #returns true yay

