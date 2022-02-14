class booze:
    # CORE COMPONENTS
    name = ""           # name of the booze
    price = ""          # price of the booze
    volume = ""         # volume (in mL) of the booze -- sometimes a multiple of a six pack (think 6 x 473)
    alc_content = ""    # alcohol content

    origin = ""         # location of origin
    brand = ""          # brand

    category = ""       # category of booze (i.e. beer, vodka, wine)
    type = ""           # type of booze (i.e. lager, ale, IPA)

    url = ""

    price_index = 0     # price index ( price / ( vol * alc_content ) )

    def __lt__(self, other):
        return self.price_index < other.price_index

    def __init__(self):
        self.name = ""
        self.price = ""
        self.volume = ""

    def __init__(self, newName, newPrice, newVolume, newAlc, newOrigin, newBrand, newCategory, newType, newUrl):
        try:
            self.name = newName.strip('"')
            self.price = float(newPrice)
            self.volume = int(newVolume)
            self.alc_content = float(newAlc)
            self.origin = newOrigin.strip('"')
            self.brand = newBrand.strip('"')
            self.category = newCategory.strip('"')
            self.type = newType.strip('"')
            self.url = newUrl.strip('"')
        except:
            self.name = "NULL"
            self.price = -1
            self.volume = -1
            self.alc_content = -1

        try:
            perc = float(newAlc) / 100
            alc_vol = float(newVolume) * float(perc)
            self.price_index = float(self.price) / float(alc_vol)
        except:
            self.price_index = 255

    def toCsv(self):
        return str( "\"" + str(self.name) + "\"" + ","
                  + "\"" + str(self.brand) + "\"" + ","
                  + "\"" + str(self.category) + "\"" + ","
                  + "\"" + str(self.type) + "\"" + ","
                  + str(self.price) + ","
                  + str(self.volume) + ","
                  + str(self.alc_content) + ","
                  + "\"" + str(self.origin) + "\"" + ","
                  + "\"" + str(self.url) + "\"" )

    def display(self):
        print(self.name)
        print("\t" + str(self.category))
        print("\t  " + str(self.type))
        print("\t" + str(self.price_index))
        print("\t$" + str(self.price))
        print("\t" + str(self.volume) + " mL -\t" + str(self.alc_content) + "%")