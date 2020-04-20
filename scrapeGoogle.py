from goslate import Goslate
import requests
from textblob import TextBlob
from pprint import pprint 
from bs4 import BeautifulSoup as bs
import random 
import time
from torrequest import TorRequest
import numpy as np

BASE_URL = "https://www.google.com"
search_item = "/search?q=news"
ANOTHER_URL = "https://www.google.com/search?q="
URL = "https://www.google.com/search?q="

headers = {"User_Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
i = 0
full_data = []
delays = [0.5, 1, 0.3, 0.7, 2, 0]

with open("news_1.py", '+w') as filehandle:
    while True:
        urls = []
        if i%10 == 0:
            tr = TorRequest(password='10BoiledCabbage')
            tr.reset_identity()
        response = tr.get(BASE_URL+search_item)
        i += 1
        if i==25:
            break

        soup = bs(response.content , "lxml")
        body = soup.body
        items = body.find_all("div", class_= "ZINbbc xpd O9g5cc uUPGi")
        for item in items:
            try:
                link = item.find("div", class_= "BNeawe UPmit AP7Wnd").get_text()

                link = link.replace("https://www.","")
                link = link.replace("http://www.","")
                link = link.replace("https://","")
                link = link.replace("http://","")
                link = link.split('›')[0]

                seo_description = item.find('div', class_ = "BNeawe s3v9rd AP7Wnd").get_text()
                temp = []
                temp.append(link)
                temp.append(seo_description)
                urls.append(temp)
            except AttributeError as AE:
                pass
        
        
        # while True:
        #     # Search each link in urls individually

        full_data.extend(urls)
        try:
            search_item = body.find_all("a", class_="nBDE1b G5eFlf" )[-1]['href']  
        except:
            break

    filehandle.writelines("ListOfData = %s" %  full_data)
# tr = TorRequest(password='10BoiledCabbage')
# tr.reset_identity()

# for x,data in enumerate(full_data,1):
#     if x%15==0:
#         tr = TorRequest(password='10BoiledCabbage')
#         tr.reset_identity()

#     # delay = np.random.choice(delays)
#     # time.sleep(delay)

#     link = data[0]
#     response = tr.get(ANOTHER_URL+link)
#     soup = bs(response.content , "lxml")
#     body = soup.body
#     try:
#         description = body.find("div", class_="Ap5OSd").get_text()
#     except ConnectionRefusedError as CE:
#         print("Connection refused!")
#     except:
#         print("Some error occured!")
#     # text = data[1]  
#     # b = TextBlob(text)
#     # if b.detect_language() != "en":
#     #     gs = Goslate()
#     #     data[1] = gs.translate(seo_description, 'en')
#     data.append(description)

