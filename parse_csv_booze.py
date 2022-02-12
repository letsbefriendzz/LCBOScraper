import booze
import operator

booze_file = "booze.csv"

def open_booze(file_name):
    return_booze = []
    with open(file_name, "r") as f:
        booze_csv = f.read()
        booze_csv = booze_csv.strip('\n')
        nodes = booze_csv.split('\n')
        for node in nodes:
            if node.split().count != 0:
                name            = node.split(',')[0]
                price           = node.split(',')[1]
                volume          = node.split(',')[2]
                alc_content     = node.split(',')[3]
                return_booze.append( booze.booze( name,price,volume,alc_content ) )
    
    return return_booze

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
        index += 1