#! /usr/bin/env python

"To get current date and check for all entries which are within 1 week from today. Give a notification of all the names as a pop-up to the user. This program will be set on cronjob of every 7 days."

import datetime as dt
import os
import json
from config import BIRTHDAY_FILE, HOME

os.environ["DISPLAY"] = ":0.0"
os.environ["XAUTHORITY"] = HOME+ ".Xauthority"

def message(title, message):
  os.system('notify-send  -u low "'+title+'" "'+message+'"')

def notify_dates():
    current_date = dt.datetime.today()

    with open(BIRTHDAY_FILE, 'r') as check_file:
        data = json.load(check_file)
        # print(data)
        for i in range(8): # <i> will be used as timedelta ranging from 0 to 7 days. 7th day is intentially left to be overlapping because it might happen that the 7th day had someone's birthday but due to no use of PC of the 7th day, the cronjob couldn't work that day. It would lead to failure of the intended cause.
            new_date = (current_date+dt.timedelta(days=i)).strftime("%d-%m")
            if data.get(new_date)!=None:
                d = dt.datetime.strptime(new_date, "%d-%m")
                month = d.strftime("%B")
                day = d. strftime("%d")
                result = ""
                result += day+" " + month+" : "
                result += data[new_date]["name"]+ "\n"
                message("Birthday: ",result)
        # for item in data:
        #     print(data[item]['name'].split())

    # print(result)
if __name__ == "__main__":
    notify_dates()
    s = "Last checked at: {}". format(dt.datetime.now().strftime("%H:%M:%S    %d-%B"))
    print(s) 
