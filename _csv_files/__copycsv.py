import sys

if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as file:
        data = file.read()
    
    with open("_booze.csv", "a") as booze_csv:
        booze_csv.write(data)