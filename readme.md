# The LCBO Web Scraper

### Ryan, Why?

I first came to this idea sometime last summer, when my curiosity regarding webscraping was at its peak. I was webscraping various websites with success (YouTube, HLTV), however LCBO.com always came back and dished me a 403. As quickly as my enthusiasm had came for the project, it was gone. Off to other projects, I guess.

Fast forward to a few days ago -- it's my 2B term, I'm living in residence, and my roommate and a friend are discussing cost effective alcohol. We can't settle on what it would be, but man, wouldn't we love to know, being the broke students we are.

Naturally, I return to the previously failed project -- and there it is again, the same 403 error that cursed me so many moons ago. But this time, I had a little bit more knowledge of how the web works. With a little bit of luck and some logical deduction, I was able to establish that the Python library I was using for making the HTTP request to the LCBO.com website -- *requests* -- was somehow telling the LCBO servers that it is a robot.

\<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN"> <br>
\<html><head> <br>
\<title>403 Forbidden</title> <br>
\</head><body> <br>
\<h1>Forbidden</h1> <br>
\<p>You don't have permission to access <web link> on this server.</p> <b>
### Enter, the ***User-Agent*** HTTP header.

The User-Agent HTTP header lets the recipient know some basic information about the device that is sending the request. I don't know what the User-Agent field that the *requests* library is sending looks like, but it's probably telling the server through this field.

Enter the spoof:

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
  
And just like that, status code 200.
We're in.
