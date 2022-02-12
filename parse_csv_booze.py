from multiprocessing import allow_connection_pickling
from ssl import OP_NO_RENEGOTIATION
from traceback import print_exception
from unicodedata import category
import booze
import operator
import sys

booze_file = "booze.csv"

def open_booze(file_name):
    return_booze = []
    with open(file_name, "r") as f:
        booze_csv = f.read()
        booze_csv = booze_csv.strip('\n')
        nodes = booze_csv.split('\n')
        for node in nodes:
            if node.split().count != 0:
                print(node.split(','))
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
    if index < 25 and i.name != "NULL":
        print(str(index+1) + ".  " + i.name)
        print("\t" + str(i.price_index))
        print("\t$" + str(i.price))
        print("\t" + str(i.volume) + " mL -\t" + str(i.alc_content) + "%")
        print("\t" + str(i.url))
        index += 1