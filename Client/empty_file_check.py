

import pandas as pd
import csv


filename = ()#need to do function to import and test files
ans = True

#might need a while loop for all of the validation files

def emptyfile(filename,ans):

    df = pd.read_csv(filename)
    df.empty # will return True if the dataframe is empty or False if not.
    ans = df.empty
    
    if ans == True:
        print()
        # insert function that logs invalid files
    else:
        print()
        #insert function for next file
        
        
        
    