#! /usr/bin/env python
import json
import os,sys
import subprocess
import time
import random 
from datetime import date, datetime, timedelta
from PIL import Image
import numpy as np
import processreader
from matplotlib import pyplot as plt
from timeit import timeit
from tldextract import extract
from config import BIRTHDAY_FILE, CATEGORIZATION_FILE, HISTORY_FILE, DAILY_ACTIVITY_PATH
# from youtube_scraping import find_category

os.environ["DISPLAY"] = ":0.0"
os.environ["XAUTHORITY"] = "/home/raj/.Xauthority"


""" 
Format of timer.json(which has data for every day):
{
    "website": {site1: 2, site2: 8, site3: 1, ...},
    "offline" : {activity1:2, activity2:1, activity3:7, ...}
}
 """

""" 
Format of timer.json(which has data for every day):
{
    "1": 14,
    "2":98,
    "3":31,
    "4":16,
    "uncategorised":{ "website": {
                                            domain: {
                                                "site": [ site1, site2, ..],
                                                "count" : 4
                                                          }
                                                }
                                            },
                                "offline" : {
                                                "activity1" : 17,
                                                "activity2" : 8,
                                                 },
                                "total": 29 (4+17+8)
                                }
    "last_updated":"13:45:03"
}
 """


def display(dic, yesterday):
    """ Function to display total time consumed in all the categories as bar chart """

    # Load the categorisation file, to find each activity or domain mapped to their respective category.
    x, y = ["Acad.", "Non-Acad.", "Entert.", "Misc.","Unknown"], []
    for k, v in dic.items():
        if k!="last_updated":
            y.append(v)
    # print(x,y)
    pos = np.arange(len(x))
    plt.bar(pos, y, color="blue", edgecolor="black")
    plt.xticks(pos, x)
    # plt.xlabel("Activity", fontsize=10)
    plt.ylabel("Time(mins)", fontsize=10)
    plt.title("{} activity : {} mins".format(yesterday, sum(y)), fontsize=20)
    # plt.show()
    if not os.path.exists(DAILY_ACTIVITY_PATH):
        os.makedirs(DAILY_ACTIVITY_PATH)

    plt.savefig(DAILY_ACTIVITY_PATH +str(yesterday)+".png", bbox_inches='tight')
    try:
        img = Image.open(DAILY_ACTIVITY_PATH+str(yesterday)+".png")
        img.show()
    except:
        pass 
    # time.sleep(1)


# Fetch active window every 5 minutes, and add 5 minutes to activity-time whenever one is detected.
get = lambda cmd: subprocess.check_output(cmd).decode("utf-8").strip()

def browser_activity():
    """ Returns the website name which is active in the firefox browser. Sample output : "www.facebook.com/video?=vxyaz3r4" """
    tab_url = ""
    # print(subprocess.check_output(["xdotool" ,"getactivewindow", "getwindowname"]).decode("utf-8"))
    current_title = "-".join(subprocess.check_output(["xdotool" ,"getactivewindow", "getwindowname"]).decode("utf-8").strip().split("-")[:-1]).strip()
    if current_title !="":
        # print(current_title)
        data_dic = processreader.fetch_links_firefox()
        if data_dic.get(current_title)==None: #Either the user is using private browser or firefox database is not yet updated.
            time.sleep(30) # wait for 30 seconds and re-fetch the firefox database.
            data_dic = processreader.fetch_links_firefox()

        if data_dic.get(current_title)!=None: # if Found return the 
            my_link = data_dic[current_title]
            # tab_url = extract(my_link).domain
            if my_link.strip()!="":
                return my_link

    return None # return None if any of the above condition fails. Indicates either db-error or private window. 

def do_the_work():
    # sleep for a random time between [0-4] mins 
    random_minute = random.randint(0,4)
    time.sleep(random_minute*60)

    today_date = date.today().strftime("%d-%m-%Y")
    # print("Updation date: ", today_date)
    update_time = datetime.now().time().strftime("%H:%M:%S")
    categorisation_data = json.load(open(CATEGORIZATION_FILE,"r")) # dictionary having all categorized data

    try:    
        timer_dic = json.load(open("/home/raj/Documents/scheduler/timer.json", "r")) #Dictionary with all daily activity data.
    except :
        timer_dic = {}

    if timer_dic.get(today_date) == None: # When about to create a new entry on today's date

        previous_date = (date.today() - timedelta(days=1)).strftime("%d-%m-%Y")
        i=2
        # Find the last accessible date within 1 month from today_date.
        while timer_dic.get(previous_date) == None and i<=30: # 
            previous_date = (date.today() - timedelta(days=i)).strftime("%d-%m-%Y")
            i+=1
        
        if timer_dic.get(previous_date) !=None: # if any date withing 30 days found in database which isn't processed yet.

            reference_dict = timer_dic[previous_date]
            
            
            # Add uncategorised activities into the browser_history_log  
            if reference_dict["uncategorised"]["total"]!=0:
                try:
                    perm_dic = json.load(open(HISTORY_FILE, "r")) # dictionary having browser history data

                except : # File not yet created or deleted by external agent
                    perm_dic={}
                    perm_dic["website"] = {}
                    perm_dic["offline"] = {}
                # For all uncategorised "website" 
                for my_domain in reference_dict["uncategorised"]["website"]:
                    perm_dic["website"][my_domain] = perm_dic["website"].get(my_domain,{})
                    perm_dic["website"][my_domain]["sites"] = perm_dic["website"][my_domain].get("sites", [])

                    perm_dic["website"][my_domain]["sites"].extend(reference_dict["uncategorised"]["website"][my_domain]["site"])
                    # removing all duplicates
                    perm_dic["website"][my_domain]["sites"] = list(set(perm_dic["website"][my_domain]["sites"])) 
                    perm_dic["website"][my_domain]["count"] = perm_dic["website"][my_domain].get("count",0) + reference_dict["uncategorised"]["website"][my_domain]["time"]

                for activity, cnt in reference_dict["uncategorised"]["offline"].items():
                    perm_dic["offline"][activity] = perm_dic["offline"].get(activity,0) + cnt 

                json.dump(perm_dic, open(HISTORY_FILE, "w+"))

            reference_dict["uncategorised"] = reference_dict["uncategorised"]["total"]
            
            # Give notification whenever unknown time exceeds 30% of other time.
            categorized_time = reference_dict["1"] +reference_dict["2"]+reference_dict["3"]+reference_dict["4"]
            uncategorized_time =  reference_dict["uncategorised"]
            if uncategorized_time > 0.5 * categorisation_data: # give red alert for categorization
                os.system('notify-send  -t 5 -u critical "[timer]: Unknown time exceeded 50%" "Run command : \"categorize\" to categorise"')
            elif uncategorized_time > 0.3 * categorisation_data: # give normal alert for categorization
                os.system('notify-send  -t 5 -u normal "[timer]: Unknown time exceeded 30%" "Run command : \"categorize\" to categorise"')

            if os.path.isfile("/home/raj/Documents/scheduler/daily_activity/"+str(previous_date)+".png")==False:
            # Send data to display function
                display(reference_dict, previous_date)
        
        temp_dictionary={"1":0,"2":0,"3":0,"4":0} # temporary dictionary to keep all categorisation 
        temp_dictionary["uncategorised"]= {"website":{}, "offline":{}, "total":0}
       
        timer_dic[today_date] = temp_dictionary

    
    # print(dic)
    activity_time = random_minute + timer_dic.get("previous_remaining_time",0)
    try:
        p_id = (
            subprocess.check_output(["xdotool", "getactivewindow", "getwindowpid"])
            .decode("utf-8")
            .strip()
        )
        p_name = (
            subprocess.check_output(["ps", "-p", p_id, "-o", "comm="]).decode("utf-8").strip()
        )
        p_name = "gnome-terminal" if p_name=="gnome-terminal-"   else p_name
        list_browsers=["firefox-bin", "vivaldi-bin"]

        print( update_time, today_date, end=" ")
        tab=""
        if p_name in list_browsers:
            if p_name=="firefox-bin":
                tab = browser_activity()
            # Add:
            # else if p_name =="vivaldi-bin":
            # else if p_name=="chrome":
            # more options for browsers like safari, chromium, etc.

            if tab!=None and  tab.strip()!="":
                dom = extract(tab).domain
                print("Last activity was: ", dom)
                
                if dom=="google": # take cases for categorisation
                    sub =  extract(tab).subdomain
                    if sub=="www": # can be all of the 4 categories. 
                        timer_dic[today_date]["1"] +=  int(activity_time*(2/5)) 
                        timer_dic[today_date]["2"] +=  int(activity_time*(2/5))  
                        timer_dic[today_date]["4"] +=  int(activity_time*(1/5)) 
                    else: # most subdomains of google are academic while others are non-academic.
                        timer_dic[today_date]["1"] +=  int(activity_time*(3/5)) 
                        timer_dic[today_date]["2"] +=  int(activity_time*(2/5)) 
                
                elif dom=="youtube":
                        timer_dic[today_date]["2"] +=  int(activity_time*(1/5)) 
                        timer_dic[today_date]["3"] +=  int(activity_time*(2/5)) 
                        timer_dic[today_date]["4"] +=  int(activity_time*(2/5))

                elif dom in categorisation_data["websites"]:
                    timer_dic[today_date][str(categorisation_data["websites"][dom])] += activity_time
                
                else:
                    timer_dic[today_date]["uncategorised"]["website"][dom]= timer_dic[today_date]["uncategorised"]["website"].get(dom,{})
                    timer_dic[today_date]["uncategorised"]["website"][dom]["site"] = timer_dic[today_date]["uncategorised"]["website"][dom].get("site", [])
                    timer_dic[today_date]["uncategorised"]["website"][dom]["time"] = timer_dic[today_date]["uncategorised"]["website"][dom].get("time", 0)
                    timer_dic[today_date]["uncategorised"]["website"][dom]["site"].append(tab)
                    timer_dic[today_date]["uncategorised"]["website"][dom]["time"] += activity_time # to keep note that which domain is using how much time
                    timer_dic[today_date]["uncategorised"]["total"] += activity_time 
            else: # private tab in entertainment
                print("Some unloaded/private tab")
                timer_dic[today_date]["3"] +=  activity_time
                # os.system("notify-send  -u critical private")

        else:
            print("Last activity: ", p_name)
            if p_name in categorisation_data["offline"]:
                timer_dic[today_date][str(categorisation_data["offline"][p_name])] += activity_time
            else:
                timer_dic[today_date]["uncategorised"]["offline"][p_name] += activity_time
                timer_dic[today_date]["uncategorised"]["total"]+= activity_time
        

        timer_dic[today_date]["last_updated"] = update_time
        timer_dic["previous_remaining_time"] = 5- random_minute
        json.dump(timer_dic, open("/home/raj/Documents/scheduler/timer.json", "w+"))
        return True # success
    except Exception as e:
        print(e)
        return False #failure
    
if __name__ == "__main__":
    # time.sleep(3)
    status = do_the_work()
    # count = 1
    # while status!= True: # until success retry
    #     time.sleep(1) # sleep for 1 sec and expect the same error to not occur again
    #     status = do_the_work()
    #     count+=1
    #     if count ==10: # try only 10 times at max
    #         break 
