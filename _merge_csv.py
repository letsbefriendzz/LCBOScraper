import sys
import booze
import time

path = "_merge_csv_test"
file1 = ""
file2 = ""

def merge():
    if len( sys.argv ) < 3:
        print("Invalid parameter set!")
        print("call with _merge_csv.py \"Parent File\" \"Category File\"")

    # We're opening two files -- a parent category file, assuming that the category itself contains
    # all subcategory instances, plus an unknown quantity that exist within the parent category but
    # not the subcategory. Thus, for the subcategory fields we can offer NULL.
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]

        missing_from_file2 = []

        with open(file1, "r") as f1:
            with open(file2, "r") as f2:
                file1_data = f1.read().split('\n')
                file2_data = f2.read().split('\n')

                # this code (((might))) break if a smaller file is used in the outer loop...
                i = 0
                for entry in file1_data:
                    match = False
                    for entry2 in file2_data:

                        e1_name = entry.split(',')[0]
                        e2_name = entry2.split(',')[0]

                        if e1_name == e2_name:
                            match = True

                    if match == False:
                        name            = entry.split(',')[0]
                        brand           = entry.split(',')[1]
                        category        = entry.split(',')[2]
                        type            = entry.split(',')[3]
                        price           = entry.split(',')[4]
                        volume          = entry.split(',')[5]
                        alc_content     = entry.split(',')[6]
                        origin          = entry.split(',')[7]
                        url             = entry.split(',')[8]
                        missing_from_file2.append( booze.booze( name,price,volume,alc_content,origin,brand,category,type,url ) )
                        i += 1

                print(i)
                time.sleep(3)

        for result in missing_from_file2:
            with open(file2, "a") as write_file:
                print("Writing " + str(result.name) + " to " + str(file2))
                write_file.write((result.toCsv()) + "\n")

def checkForDupes():
    file1 = sys.argv[1]
    with open(file1, 'r') as in_file, open('ouput.csv','w') as out_file:
    
        seen = set() # set for fast O(1) amortized lookup
        
        for line in in_file:
            if line in seen: 
                continue # skip duplicate

            seen.add(line)
            out_file.write(line)

checkForDupes()