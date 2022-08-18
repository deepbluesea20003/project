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
import time

#this is a self-contained function that only needs to be written once in the final program to save execution time
#& less likely to have a file-handling error

#want to make separate function but keep getting I/O on closed file error message
##def read_in_file(filename):
##    with open(filename) as med_file:
##        csv_reader = csv.DictReader(med_file)
##    return csv_dict


def value_checks(filename):
    valid_file = True
    #csv_dictionary = read_in_file(filename)
    with open(filename) as med_file:
        csv_reader = csv.DictReader(med_file)
        for row in csv_reader:
            for key, value in row.items():
                #validate the timestamp is valid
                if key == 'timestamp':
                    try:
                        time.strptime(value[:8], '%H:%M:%S')
                    except ValueError:
                        print("time failed \n", row)
                        valid_file = False
                #validate the reading values
                elif key.startswith('reading'):
                    #convert to float as initial check and for later comparisons
                    try:
                        value = float(value)
                    except:
                        print("float failed \n", row)
                        valid_file = False
                    else:
                        #checks within bounds
                        if (value < 0)  or (value > 9.9):
                            print("value bounds failed \n", row)
                            valid_file = False
                        #checks 3 decimal points
                        else:
                            nums = str(value)[::-1].find('.')
                            if nums > 3:
                                print("num of dec places failed \n", row)
                                valid_file = False
    return valid_file


#tests
#never failed the more than 3 decimal places - is that working?
 #do more testing against decimal places check to make sure works 
print(value_checks("MED_DATA_20210701153942.csv")) 
print(value_checks("MED_DATA_20210701153947.csv"))
print(value_checks("MED_DATA_20210701153948.csv"))
print(value_checks("MED_DATA_20210701153952.csv"))
print(value_checks("MED_DATA_20210701153954.csv"))
                
    
