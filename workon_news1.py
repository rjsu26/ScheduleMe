from torrequest import TorRequest
from news_1 import ListOfData
from random import random
from bs4 import BeautifulSoup as bs
import numpy as np
import time
# print(ListOfData)

ANOTHER_URL = "https://www.google.com/search?q="
tr = TorRequest(password='10BoiledCabbage')
tr.reset_identity()
lnght = len(ListOfData)
x = 0
delays = [random() for _ in range(10)]*5

with open("news_2.py", "w") as fo:
    fo.writelines("BetterData = [\n")
    while True:
        if x>= lnght:
            break
        if x%8==0:
            tr = TorRequest(password='10BoiledCabbage')
            tr.reset_identity()

        link = ListOfData[x][0]

        response = tr.get(ANOTHER_URL+link)
        soup = bs(response.content , "lxml")
        body = soup.body
        error_count = 0

        if error_count >= 5:
            print("Restarting from %d"%(x-5))
            x = x-5
        
        else:
            try:
                description = body.find("div", class_="Ap5OSd").get_text()
                error_count = 0
                ListOfData[x].extend(description)
                fo.writelines("%s,\n"%ListOfData[x])
            except ConnectionRefusedError as CE:
                print("Connection refused!")
                error_count += 1
            except:
                print("Some error occured!")
                error_count += 1
            x += 1
        
        delay = np.random.choice(delays)
        time.sleep(delay)
        # text = data[1]  
        # b = TextBlob(text)
        # if b.detect_language() != "en":
        #     gs = Goslate()
        #     data[1] = gs.translate(seo_description, 'en')


