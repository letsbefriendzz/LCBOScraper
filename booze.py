from time import process_time_ns
from traceback import print_exception
from unicodedata import name


class booze:
    name = ""
    price = ""
    volume = ""
    alc_content = ""
    price_index = 0

    def __init__(self):
        self.name = ""
        self.price = ""
        self.volume = ""

    def __init__(self, newName, newPrice, newVolume, newAlc):
        self.name = newName
        self.price = newPrice
        self.volume = newVolume
        self.alc_content = newAlc

        try:
            perc = newAlc / 100
            self.price_index = self.price / ( self.volume * perc )
        except:
            self.price_index = -1
