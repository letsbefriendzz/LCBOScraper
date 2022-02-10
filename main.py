from ast import excepthandler
from os import times_result
from pyexpat.errors import XML_ERROR_ABORTED
import matplotlib.pyplot as plt
import numpy as np

from asyncio.windows_events import NULL
from logging import BufferingFormatter
from bs4 import BeautifulSoup
import requests
import time

import booze

# SCRAPE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
booze_types = {
                "vodka":    "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/vodka-15019?pageView=grid&orderBy=5&beginIndex=",
                "rum":      "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/rum-15016?pageView=grid&orderBy=5&beginIndex=",
                "gin":      "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/gin-15014?pageView=grid&orderBy=5&beginIndex=",
                "tequila":  "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/tequila-15018?pageView=grid&orderBy=5&beginIndex=",
                "whisky":   "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky?pageView=grid&orderBy=5&beginIndex="
            }

wine = {"red": "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/wine-14/wine-14/red-wine-14001?pageView=grid&orderBy=5&beginIndex=",
        "white": "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/wine-14/wine-14/white-wine-14002?pageView=grid&orderBy=5&beginIndex="}

# Array to store booze results
results = []

def scanForBooze(type):
    begin_index = 0
    while True:
        page = requests.request("GET", booze_types[type]
                        + str(begin_index),
                        headers={"User-Agent":UA})

        s = BeautifulSoup(page.text, 'html.parser')
        prices = s.find_all("div", {"class": "col-xs-7 product_info product-info-section"})
        # SCRAPE

        print("scraping \""+type+"\" @ index " + str(begin_index) + "\t" + str(page.status_code))

        i = 0
        for p in prices:
            liq_volum = str(p.find('div', {'class': 'other_details'}).find_next('span').text.strip().split('m', 1)[0])
            liq_title = str(p.find('a', {'tabindex': '0'}).text)

            # alc % acquisition
            liq_url = str(p.find('a', {'tabindex': '0'})['href'])
            liq_page = requests.request("GET", liq_url, headers={"User-Agent":UA})
            lp = BeautifulSoup(liq_page.text, 'html.parser')

            details = lp.find('dl', {'class': 'product-details-list'}).text
            percentage = float(details.split('Alcohol/Vol:')[1].split('%')[0].strip())
 
            try:
                liq_price = str(p.find('span', {'class': 'price'}).text.strip().strip('$'))
                liq_price = liq_price.replace(',', '')
                liq_price = float(liq_price)
            except:
                print("error parsing price -> float")
                liq_price = str(p.find('span', {'class': 'price'}).text.strip().strip('$'))
            results.append(booze.booze(liq_title, liq_price, liq_volum, percentage))
            i += 1
        
        if i == 0 or page.status_code != 200 or begin_index == 12:
            break

        begin_index = begin_index + 12

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

# MAIN THREAD
start_time = time.time()
for i in booze_types:
    if i == "tequila":
        scanForBooze(i)

end_time = time.time()

time_elapsed = end_time - start_time
time_convert(time_elapsed)

price_indices = []
volumes = []
names = []
for r in results:
    price_indices.append(float(r.price_index))
    volumes.append(float(r.volume))
    names.append(r.name)

fig, ax = plt.subplots()

ax.plot(price_indices, volumes, 'o', color='black')

# set titles

for i, txt in enumerate(names):
    if price_indices[i] <= 0.0375:
        ax.annotate(txt, (price_indices[i], volumes[i]))

ax.set(xlabel="Price Index - $/alc%", ylabel="Volume", title="Student Chart of Alcoholism")
plt.legend()
plt.show()