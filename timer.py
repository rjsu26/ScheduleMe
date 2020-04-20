#! /usr/bin/env python
import json
import os,sys
import subprocess
import time
from datetime import date, datetime, timedelta
from PIL import Image
import numpy as np
import processreader
from matplotlib import pyplot as plt
from timeit import timeit
from tldextract import extract


os.environ["DISPLAY"] = ":0.0"
os.environ["XAUTHORITY"] = "/home/raj/.Xauthority"

# time.sleep(4)

def display(dic, yesterday):
    """ Function to display total time consumed in all the apps as bar chart """

    x, y = [], []
    for k, v in dic.items():
        if k == "last_updated" or k=="browser" or k=="tab" :
            continue
        # print(k, v)
        x.append(k)
        y.append(v)
    # print(x,y)
    pos = np.arange(len(x))
    plt.bar(pos, y, color="blue", edgecolor="black")
    plt.xticks(pos, x)
    plt.xlabel("Activity", fontsize=10)
    plt.ylabel("Time(mins)", fontsize=10)
    plt.title("{} 's Laptop activity distribution".format(yesterday), fontsize=20)
    # plt.show()
    plt.savefig( "/home/raj/Documents/scheduler/daily_activity/"+str(yesterday)+".png", bbox_inches='tight')
    try:
        img = Image.open("/home/raj/Documents/scheduler/daily_activity/"+str(yesterday)+".png")
        img.show()
    except:
        pass 
    # time.sleep(1)


# Fetch active window every 5 minutes, and add 5 minutes to activity-time whenever one is detected.
get = lambda cmd: subprocess.check_output(cmd).decode("utf-8").strip()

def browser_activity():
    """ Returns the website name which is active in the firefox browser. Sample output : "facebook" """
    tab_url = ""
    # print(subprocess.check_output(["xdotool" ,"getactivewindow", "getwindowname"]).decode("utf-8"))
    current_title = "-".join(subprocess.check_output(["xdotool" ,"getactivewindow", "getwindowname"]).decode("utf-8").strip().split("-")[:-1]).strip()
    if current_title !="":
        # print(current_title)
        data_dic = processreader.fetch_links_firefox()
        if data_dic.get(current_title)!=None: # checking for worse case if title not present in dictionary
            my_link = data_dic[current_title]
            tab_url = extract(my_link).domain
            if tab_url.strip()!="":
                return tab_url.lower()

def do_the_work():
    today_date = date.today().strftime("%d-%m-%Y")
    update_time = datetime.now().time().strftime("%H:%M:%S")

    timer_dic = {}
    try:
        timer_dic = json.load(open("/home/raj/Documents/scheduler/timer.json", "r"))
    except :
        pass

    if timer_dic.get(today_date) == None: # When about to create a new entry on today's date
        yesterday = (date.today() - timedelta(days=1)).strftime("%d-%m-%Y")
        if timer_dic.get(yesterday) != None: # if previous day's data is avaliable
            # open the history log file and increment count of all websites present under "browser" key. E.g history["springer"]++,  etc. 
            perm_dic={}
            try:
                perm_dic = json.load(open("/home/raj/Documents/scheduler/browser_history_log.json", "r"))
            except : # File not yet created or deleted by external agent
                pass        
            if timer_dic[yesterday].get("browser")!=None:
                for k in timer_dic[yesterday]["browser"].keys():
                    if k!="private":
                        perm_dic[k] = perm_dic.get(k, {})
                        perm_dic[k]["count"] = perm_dic[k].get("count",0) + (int)(timer_dic[yesterday]["browser"].get(k,0)/5)

            json.dump(perm_dic, open("/home/raj/Documents/scheduler/browser_history_log.json", "w+"))

            display(timer_dic[yesterday], yesterday)
        timer_dic[today_date] = {}

    # print(dic)
    try:
        p_id = (
            subprocess.check_output(["xdotool", "getactivewindow", "getwindowpid"])
            .decode("utf-8")
            .strip()
        )
        p_name = (
            subprocess.check_output(["ps", "-p", p_id, "-o", "comm="]).decode("utf-8").strip()
        )
        p_name = "gnome-terminal" if "gnome-terminal" in p_name else p_name
        list_browsers=["firefox-bin", "vivaldi-bin"]

        tab=""
        if p_name in list_browsers:
            if p_name=="firefox-bin":
                tab = browser_activity()
            # Add:
            # else if p_name =="vivaldi-bin":
            # else if p_name=="chrome":
            # more options for browsers like safari, chromium, etc.

            timer_dic[today_date]["browser"] = timer_dic[today_date].get("browser",{}) 
            if tab!=None and  tab.strip()!="":
                timer_dic[today_date]["browser"][tab] = timer_dic[today_date]["browser"].get(tab,0) + 5
            else:
                timer_dic[today_date]["browser"]["private"] = timer_dic[today_date]["browser"].get("private",0) + 5
                os.system("notify-send  -u critical private")


        else:
            timer_dic[today_date][p_name] = timer_dic[today_date].get(p_name, 0) + 5
        

        timer_dic[today_date]["last_updated"] = update_time
        json.dump(timer_dic, open("/home/raj/Documents/scheduler/timer.json", "w+"))
        return True # success
    except Exception as e:
        sys.stderr.write("ERROR", e)
        return False #failure
    
if __name__ == "__main__":
    # print(timeit(do_the_work,number = 1000))
    # time.sleep(1)
    status = do_the_work()
    count = 1
    while status!= True: # until success retry
        time.sleep(1) # sleep for 1 sec and expect the same error to not occur again
        status = do_the_work()
        count+=1
        if count ==10: # try only 10 times at max
            break 
