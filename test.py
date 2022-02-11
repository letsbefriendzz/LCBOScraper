import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
url = "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/wine-14/red-wine-14001/anselme-la-fiole-du-pape-chateauneuf-du-pape-aoc-12286"
page = requests.request("GET", url,
                headers={"User-Agent":UA})

print(page.status_code)