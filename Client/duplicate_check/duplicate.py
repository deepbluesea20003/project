# Check for duplicate batch ids
# adam

# Sees if there are any duplicated IDs with a csv file

def checkUniqueBatchIDs(fileName):
    # lovely bit of formatting
    file = open(fileName, "r")
    lines = [i.replace("\n", "").split(",") for i in file.readlines()]

    # read in all batch ids
    ids = [i[0] for i in lines]

    # returns true if all ids are unique, false if not
    return len(ids) == len(set(ids))


