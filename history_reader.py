""" Program to read all history from all available browsers in the system and use their frequency count for categorization purpose. To be used as cron job set to once every month. After processing, the history will be deleted i.e. moz_places tables will be redacted. """

import os
import sqlite3
import tldextract 
import subprocess
import glob
import pprint
import json 
import time
import datetime

# name of the file where processed history is kept
HISTORY_FILE = "browser_history_log.json"

def find_all_browsers():
    """ scan /usr/share/applications folder for all applications with WebBrowser in Categories field"""    
    application_path = "/usr/share/applications/"
    files = os.listdir(application_path)
    list_of_browsers=[]
    for file in files:
        try:
            file_path = application_path+file
            data = subprocess.Popen(["cat",file_path], stdout=subprocess.PIPE)
            grep = subprocess.Popen(["grep", "WebBrowser"],stdin=data.stdout,stdout=subprocess.PIPE)
            out = grep.communicate()[0].decode('utf-8').strip()
            if out!="":
                data = subprocess.Popen(["cat",file_path], stdout=subprocess.PIPE)
                name_pipe = subprocess.Popen(["grep", "Name="], stdin=data.stdout, stdout=subprocess.PIPE)
                name = name_pipe.communicate()[0].decode('utf-8').strip().splitlines()[0]
                list_of_browsers.append(name[5:])
        except:
            pass
    
    return list_of_browsers

def firefox_history_scan(file_name):
    prev_data = {}
    try:
        prev_data=json.load(open(file_name, "r"))
    except:
        pass
    data_path = os.path.expanduser('~')+"/.mozilla.old/firefox/*.default/"
    all_possible_paths = glob.glob(data_path)
    location = "places.sqlite"
    history_path = [x+location for x in all_possible_paths]
    for path in history_path:
        try:
            c = sqlite3.connect(path)
            cursor = c.cursor()

            select_statement = "select moz_places.url, moz_places.visit_count from moz_places;"
            cursor.execute(select_statement)
            results = cursor.fetchall()

            for url, count in results:
                url_object = tldextract.extract(url)
                subdomain = url_object.subdomain + "." if url_object.subdomain.strip()!="" else "" 
                domain = url_object.domain + "." if url_object.domain.strip()!="" else ""
                suffix = url_object.suffix  if url_object.suffix.strip()!="" else ""
                main_url = "{}{}{}".format(subdomain, domain, suffix)
                domain = url_object.domain
                if domain.strip()!="":
                    domain = domain.lower()
                    prev_data[domain] = prev_data.get(domain,dict())
                    prev_data[domain]["sites"] = prev_data[domain].get("sites",list())
                    if main_url not in prev_data[domain]["sites"]: 
                        prev_data[domain]["sites"].append(main_url)
                    prev_data[domain]["count"]=prev_data[domain].get("count",0) + count

        except Exception as e:
            print("ERROR", e)
            print()
    json.dump(prev_data,open(file_name,"w+"), indent=4)
    return prev_data

if __name__ == "__main__":
    data_dic = firefox_history_scan(HISTORY_FILE)
    # Sort the data_dic as per count
