# LCBO Web Scraper
## The Quest for Cost Efficient Booze

### Ryan, Why?

I first came to this idea sometime last summer, when my curiosity regarding webscraping was at its peak. I was webscraping various websites with success (YouTube, HLTV), however LCBO.com always came back and dished me a 403. As quickly as my enthusiasm had came for the project, it was gone. Off to other projects, I guess.

Fast forward to a few days ago -- it's my 2B term, I'm living in residence, and my roommate and a friend are discussing cost effective alcohol. We can't settle on what it would be, but man, wouldn't we love to know, being the broke students we are.

Naturally, I return to the previously failed project -- and there it is again, the same 403 error that cursed me so many moons ago. But this time, I had a little bit more knowledge of how the web works. With a little bit of luck and some logical deduction, I was able to establish that the Python library I was using for making the HTTP request to the LCBO.com website -- *requests* -- was somehow telling the LCBO servers that it is a robot.

### Enter, the ***User-Agent*** HTTP header.

The User-Agent HTTP header lets the recipient know some basic information about the device that is sending the request. I don't know what the User-Agent field that the *requests* library is sending looks like, but it's probably telling the server through this field.

Enter the spoof:

`UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"`
  
Pass that as a parameter in my request call, and just like that, status code 200.

***We're in.***

### How's it work?
  
Because the LCBO website is well designed and consistent, I quickly realized that every search category would display all the contents of the given category, in groups of 12 items per page. What search page we were on is dictated by an element in the GET query string that's present in the url.
  
#### The URL
  
The query string always looked like this:
  
`?pageView=grid&orderBy=5&beginIndex=`
  
With beginIndex defining the index of the search results at which the page will begin at. My guess is that the server generates an array of results, and this beginIndex is literally the index it's ripping from. Not a very adventurous guess.

**When you travel forwards or backwards by a page in the serach results, beginIndex iterates by +-12**.

This query string is a constant suffix on every category. Wonderful. All I've got to do is compile every category and every subcategory into a nested dictionary, call each URL with my webscraping code, and send the results to an appropriately named CSV file.

#### The Webscraping Code

The code itself is super simple, but needed a fair amount of tweaking and is absolutely illegible (by my standards) if it weren't for my commenting. Each element that I'm tracking (name, brand, category, subcategory, price, volume, alcohol content, origin location) needed to be meticulously extracted using lots of `split` and `strip` method calls. BeautifulSoup is really a wonderful library and made this process insanely easy.

More info can be found in the comments of `lcbo_scrape.py`, which contains the main webscraping code.
