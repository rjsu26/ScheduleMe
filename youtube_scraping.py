""" To scrape a youtube page to find the category of the video being played currently. """
import requests
from bs4 import BeautifulSoup 
import time 

""" 
Category_index = {
     'Film & Animation':1,
     'Autos & Vehicles':2,
     'Music': 3,
     'Pets & Animals': 4,
     'Sports': 5,
     'Travel & Events': 6,
     'Gaming': 7,
     'People & Blogs': 8,
     'Comedy': 9,
     'Entertainment': 10,
     'News & Politics': 11,
     'Howto & Style': 12,
     'Education': 13,
     'Science & Technology': 14,
     'Nonprofits & Activism': 15} """

# fail_count = 0 #if fail count ==3 break and return false.

def find_category(link):
    """ Returns the category of video being played in youtube. Returns 0 when no category is found for any reason."""
    try:
        url = link 
        source= requests.get(url).text
        soup=BeautifulSoup(source,'lxml')
        if soup==None:
            return "0"
        category = soup.findAll('ul', class_="content watch-info-tag-list")
        if category==[]:
            return "0"
        category = category[0].text.strip(' \n')
        # print(category)
        return category
    except Exception as e:
        # print(e)
        return "0"

if __name__=="__main__":
    link = "https://www.youtube.com/"
    for _ in range(100):
        s = time.time()
        print(find_category(link))
        print(time.time()-s)
