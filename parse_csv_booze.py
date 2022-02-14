import matplotlib.pyplot as plt
import numpy as np
import booze
import operator
import sys

booze_file = "booze.csv"

def open_booze(file_name):
    return_booze = []
    with open(file_name, "r") as f:
        booze_csv = f.read()
        print("Scanning " + str( len( booze_csv.split('\n') ) ) + " records" )
        booze_csv = booze_csv.strip('\n')
        nodes = booze_csv.split('\n')
        for node in nodes:
            if node.split().count != 0:
                name            = node.split(',')[0]
                brand           = node.split(',')[1]
                category        = node.split(',')[2]
                type            = node.split(',')[3]
                price           = node.split(',')[4]
                volume          = node.split(',')[5]
                alc_content     = node.split(',')[6]
                origin          = node.split(',')[7]
                url             = node.split(',')[8]
                return_booze.append( booze.booze( name,price,volume,alc_content,origin,brand,category,type,url ) )
    
    return return_booze

# Main Threads

if len(sys.argv) > 1:
    booze_file = sys.argv[1]
alcohol = open_booze(booze_file)
alcohol.sort(key=operator.attrgetter('price_index'))

index = 0
displayed = 0
for i in alcohol:
    if index < 25:# and i.category.__contains__('Wine') != True:
        print(index + 1)
        i.display()
        index += 1

price_indices = []
volumes = []
names = []
for r in alcohol:
    if r.price_index <= 0.2:
        if price_indices.__contains__(float(r.volume)) != True and volumes.__contains__(float(r.volume)) != True:
            names.append(r.name)
            volumes.append(float(r.volume))
            price_indices.append(float(r.price_index))   

fig, ax = plt.subplots()

ax.plot(price_indices, volumes, 'o', color='black')

# set titles

for i, txt in enumerate(names):
    if price_indices[i] <= 5:
        ax.annotate(txt, (price_indices[i], volumes[i]))

ax.set(xlabel="Price Index - $/mL of Alcohol", ylabel="Volume", title="Student Chart of Alcoholism")
plt.legend()
plt.show()