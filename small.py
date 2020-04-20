import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from torrequest import TorRequest

url = "https://www.google.com"
search_item = "/search?q=computer+science"
tr = TorRequest(password='10BoiledCabbage')
tr.reset_identity()
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
response = tr.get(url+search_item, headers=headers)
soup = bs(response.content, "lxml")
body = soup.body
print(body.prettify())
# print()
# description = body.find("div", class_="Ap5OSd").get_text()
# print(description)
# for item in description:
#     try:
#         item2=item.find("div", class_="BNeawe s3v9rd AP7Wnd")  
#         for x,i in enumerate(item2):
#             try:
#                 item3 = i.find("div", class_="BNeawe s3v9rd AP7Wnd")
#                 print(x, item3)
#             except:
#                 pass
#     except:
#         pass
# print(description)