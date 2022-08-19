
import csv


filename = ()#need to do function to import and test files
ans = False

#program checks if file ends in csv, and no invalid symbols
#this is so long winded and ineeficient but i tried for hours to do it otherways

def name_validation(filename,ans):
    
    if ".csv" in filename:
        ans = False
    
        if "," in filename:
            ans = True
            
            if "?" in filename:
                ans = True
                
                if "," in filename:
                    ans = True
                    
                    if "/" in filename:
                        ans = True
                        
                        if ":" in filename:
                            ans = True
                            
                            if "*" in filename:
                                ans = True
                                
                                if ">" in filename:
                                    ans = True
                                
                                else:
                                    ans = False
                                
                            else: 
                                ans = False
                        else: 
                            ans = False
                    else: 
                        ans = False
                            
                else:
                    ans = False
            
            else:
                ans = False
        
        else:
            ans = False
        
 
        
    else:
        ans = True
    

    if ans == True:
        print()
        # insert function that logs invalid files
    else:
        print()
        #insert function for next file
    
   


