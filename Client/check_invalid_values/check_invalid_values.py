#purpose: check for invalid entries (e.g. reading values of 10 or greater)
#author: Ella

#what to check for in readings:
# - readings shld all be floating point numbers
# - all readings formatted up to 3 decimal places max
# - no value should exceed 9.9 -> becomes invalid data
# - no value should be below 0

#-timestamps shld all be valid (not a time that can't exist

#-assume batch_IDs good if gone thru batch_ID check already

import csv
import decimal

#this is a self-contained function that only needs to be written once in the final program to save execution time
#& less likely to have a file-handling error
def read_in_file(filename):
    with open(filename) as med_file:
        csv_reader = csv.DictReader(med_file)
    return csv_reader

def check_in_range(csv_reader):
    for row in csv_reader


def overall_readings_check(filename):
    valid_file = True
    csv_reader = read_in_file(filename)
    ##NEED TO REMOVE CHECKS AGAINST NON-READING VALUES
    for row in csv_reader:
        for value in row.values():
            #within bounds
            if (value < 0)  or (value > 9.9):
                valid_file = False
            #float type
            elif type(value) != float:
                valid_file = False
            elif (abs(value.as_tuple().exponent)) > 3:
                valid_file = False
                
    
