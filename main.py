from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from bs4 import BeautifulSoup
import requests
import time
from lcbo_data import alcohol

import booze

# SCRAPE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"

file_handle = "_csv_files\\"

# Array to store booze results
results = []

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

def write_to_file(b):
    with open(file_handle + category + ".csv", "a+") as f:
        f.write(b.toCsv() + "\n")

def scanForBooze(lcbo_url, index = 0):
    begin_index = index
    while True:

        success = False
        req_fail = 0
        while success != True:
        #{
            # make a request to our URL -- store in page
            page = requests.request("GET", lcbo_url
                            + str(begin_index),
                            headers={"User-Agent":UA})
            if page.status_code == 200:
                success = True
            else:
                print("Request failed... retrying\t" + str(req_fail) + " / 10")
                req_fail += 1

            if req_fail == 10:
                return -1
        #}

        try:
            # parse to BS object
            s = BeautifulSoup(page.text, 'html.parser')

            # extract all product data subcomponents
            product_data = s.find_all("div", {"class": "col-xs-7 product_info product-info-section"})
            # SCRAPE

            # let the user know we haven't frozen
            print("scraping \""+type+"\" @ index " + str(begin_index) + "\t" + str(page.status_code))
        except:
            product_data = ""

        i = 0
        # iterate through all results in product data
        for p in product_data:
            # EXTRACT THE LIQ VOLUME

            # find the first div with the class 'other_details' - other_details is the small bar below the liquor title
            # that contains the volume and LCBO product number. From this we want to extract the volulme.

            # the volume is stored inside a span -- unclassed and with no ID. but the first span within this parent div.
            # we're going to take te text from it using .text(), and strip any whitespace using .strip()

            # next, we split the resultant value by 'm' - since we know it'll be present, we want the value BEFORE 'm',
            # as this is the integer that represents in mL the volume of this alcohol. Finally, we strip the string that
            # we get as a result, and parse it to a string.
            liq_volum = str( p.find( 'div', {'class': 'other_details'} ).find_next('span').text.strip().split( 'm', 1 )[0].strip() )

            # sometimes, we find ourselves with a resultatnt value that is a multiple. for example, we may be scraping
            # beer and get a volume of "6 x 473 mL". Thus, we attempt to split the liq_volume string by an 'x', and see
            # if we get more than one string in the resultant array. If we do, we parse each split component to an int
            # and multiply them together to get the total volume.
            if len( liq_volum.split('x') ) > 1:
                liq_volum = int(liq_volum.split('x')[0]) * int(liq_volum.split('x')[1])

            # awkwardly, the title component has no unique identifier. lots of elements have a tabindex value of 0, but
            # the tital happens to be the first. Thus we can find the first instance of a hyperlink (<a>) with a tabindex
            # value of 0. We take the inner text component of this object as the liq_title variable.
            liq_title = str(p.find('a', {'tabindex': '0'}).text)

            # alc % acquisition
            
            # to get the alcohol percentage, we have to get the URL stored in the <a> tag that also contains our title.
            # to do this, we extract the 'href' value from the same html tag we called before.
            liq_url = str(p.find('a', {'tabindex': '0'})['href'])

            # then, we make a request to it with the same spoofed UA
            liq_page = requests.request("GET", liq_url, headers={"User-Agent":UA})
            # and parse it ao a beautifulsoup object, called lp for 'liquor page'.
            lp = BeautifulSoup(liq_page.text, 'html.parser')

            # next, we locate the description list with the tag 'product-details-list'. Then, we split the resultant text
            # string by 'Alcohol/Vol:', the label that prefaces the alcohol content, and we take the first value. We slpit
            # that by a % sign, the guaranteed follow-up to the alcohol content, and take the first substring. We strip it
            # of any potential whitespace, and use this as our alcohol content value.
            details_html = lp.find('dl', {'class': 'product-details-list'})
            details = lp.find('dl', {'class': 'product-details-list'}).text
            percentage = float(details.split('Alcohol/Vol:')[1].split('%')[0].strip())
            try:
                brand = str(details_html).split('<dt><b>By:</b></dt>')[1].split('</span></dd>')[0].split('<dd><span>')[1]
            except:
                brand = "NULL"

            try:
                origin = str(details_html).split('<dt><b>Made In:</b></dt>')[1].split('</span></dd>')[0].split('<dd><span>')[1].strip()
            except:
                origin = "NULL"
 
            # and now, for silly solutions with ryan.
            # to get our price, we look for a span with the class 'price'. really, that's it. we strip this of whitespace
            # and the preface $, and then replace any commas with whitespace so we can parse this to a float. If any of
            # this fails, we inform the user via console, and instead we just store the resultant string as the liq_price.
            try:
                liq_price = str(p.find('span', {'class': 'price'}).text.strip().strip('$'))
                liq_price = liq_price.replace(',', '')
                liq_price = float(liq_price)
            except:
                print("error parsing price -> float")
                liq_price = str(p.find('span', {'class': 'price'}).text.strip().strip('$'))

            # finally, we instantiate a new booze object and append it to our results list.
            # results.append(booze.booze(liq_title, liq_price, liq_volum, percentage, origin, brand))
            write_to_file(booze.booze(liq_title, liq_price, liq_volum, percentage, origin, brand, str(category), str(type)))
            i += 1
        
        if i == 0 or page.status_code != 200:
            break

        begin_index = begin_index + 12

# MAIN THREAD
start_time = time.time()
# category = beer, wine, vodka, etc
for category in alcohol:
    # type = lager, ale, etc
    for type in alcohol[category]:
        scanForBooze(alcohol[category][type])

"""
end_time = time.time()

time_elapsed = end_time - start_time
time_convert(time_elapsed)

price_indices = []
volumes = []
names = []
for r in results:
    if r.price_index < 0.1 and int(r.volume) > 749:
        price_indices.append(float(r.price_index))
        volumes.append(float(r.volume))
        names.append(r.name)
    

fig, ax = plt.subplots()

ax.plot(price_indices, volumes, 'o', color='black')

# set titles

for i, txt in enumerate(names):
    if price_indices[i] <= 0.075:
        ax.annotate(txt, (price_indices[i], volumes[i]))

ax.set(xlabel="Price Index - $/mL of Alcohol", ylabel="Volume", title="Student Chart of Alcoholism")
plt.legend()
plt.show()
"""