#! /usr/bin/env python

""" Program to read all history from firefox in the system and use their frequency count for categorization purpose. To be used as cron job set to once every month."""

""" 
Format of data in HISTORY_FILE(which only has uncategorised data):
{
    "website" : {
        "mozilla":{"site":["support.mozilla.com", "www.mozilla.com"], "count":19}
    },
    "offline":{"totem":7, "code":31}
}
 """

import os,sys
import sqlite3
import tldextract
import subprocess
import glob
import pprint
import json
import time
from datetime import date, timedelta
from config import HISTORY_FILE, CATEGORIZATION_FILE
menu = """ 
Categories: 
    1. Academic : Materials related to academics
    2. Non-Academic : Anything which is not exactly academic but neither entertainment like news, howto tutorials, blogging, Messaging, etc.
    3. Entertainment : Activities like music, videos, adult, etc.
    4. Miscellaneous : Activities like youtube, terminal, calculator, file explorer, software and updates, etc which can't be clearly distinguished as academic, non-academic or entertainment.

 """


def main():
    """ Main function to gather data from firefox history and system applications and prompt user to categorise them. There are 2 separate cases: one that would run during fresh installation and the other that would run at all other instances. """
    try: # to catch keyboard interrupt 
            
        categorised_data = {}
        categorised_data["website"] = {} # domain to category manpping
        categorised_data["offline"] = {}
        categorised_data["website"]["youtube"] = 4
        categorised_data["website"]["private"] = 3
        # scan for all history in firefox
        data= {"website":{}, "offline":{}}
        do_offline = True  # set to "do" for installation time running.

        try: # On normal days, when its not installation procedure, simply process the HISTORY_FILE which has been updated everyday by timer.json.
            categorised_data = json.load(open(CATEGORIZATION_FILE, "r+"))
            data = json.load(open(HISTORY_FILE, "r"))
            do_offline = False # do_offline parameter decides if categorization for offline application is to be done or not. Set to "don't do" here since its not installation-run.
        except Exception as e: # On first installation, create CATEGORIZATION_FILE and read all of history
            # print(e)
            data["website"] = firefox_history_scan(categorised_data)

        finally:
            do_the_categorization(data, categorised_data, do_offline) # Ask the user to categorize and save all the changes into the data and categorised_data dictionary.
    
    except KeyboardInterrupt:
        print("Interrupted!! Terminating..")
    except Exception as e:
        print(e)
    
    finally:
        json.dump(data, open(HISTORY_FILE, "w+"))
        json.dump(categorised_data, open(CATEGORIZATION_FILE, "w+"))


def  do_the_categorization(data, categorised_data, do_offline):
    """ Using the un-classified data and previously categorised data, prompt the user for top most visited unclassified websites and then put them inside categorised data after  removing it from the unclassified data. 
    
    Add an last_updation_date field before exiting.
    """
    
    print("\n\n[!] Starting categorising new 'Website' data in descending order.\n\n")
    time.sleep(1)

    # "website" categorisation
    for k,v in sorted(data["website"].items(), key = lambda x: x[1]["count"], reverse=True):
        os.system("clear")
        if categorised_data["websites"].get(k)==None: # if domain not categorised till now
            print("Domain : {}".format(k))
            print("Sites : ")
            for site in v["sites"]:
                print(" -   ", site)
            print("\n\n Frequency use: ", v["count"])

            print()
            print(menu)

            choice = get_choice()
            if choice==6:
                break
            elif choice==5:
                continue
            else:
                categorised_data["websites"][k]=choice 

        data["website"].pop(k,None) # remove the domain <k> from data dictionary if present, otherwise return None

    applications_dict = find_all_applications()

    if do_offline==False: # do_offline will be false when its not the installation-time run.
        """ access "offline" activities from data dictionary. """ 
        # print("I was here")
        print("\n\n[!][!] Starting offline categorisation..\n\n")
        time.sleep(1)
        for k,v in sorted(data["offline"].items(), key = lambda x: x[1] , reverse=True):
            os.system("clear")
            if k not in categorised_data["offline"]:
                print("Process: ", )
                if k in applications_dict:
                    print(applications_dict[k])
                else:
                    print(k)
                
                print("\n\n Frequency use: ", v)
                print()
                print(menu)
                choice = get_choice()
                if choice==6:
                    break
                elif choice==5:
                    continue
                else:
                    categorised_data["offline"][k]=choice 

            data["offline"].pop(k,None)

    else:    
        # "Offline" categorisation
        print("\n\n[!] Starting categorising new 'Offline' applications. \n\nJust select all those which you recognise and use frequently. You may do it later, but doing it now would increase the accuracy of the scheduler..\n\n")
        
        # time.sleep(1)

        for k,v in applications_dict.items():
            os.system("clear")
            if categorised_data["offline"].get(k)==None:
                print("Application Name: ",v)
                print()
                print(menu)
                choice = get_choice()    
                if choice==6:
                    break
                elif choice==5:
                    continue
                else:
                    categorised_data["offline"][k]=choice

    today_date = date.today().strftime("%d-%m-%Y")
    data["last_updated"] = today_date
    return

def get_choice():
    """ Ask user to input any number between 1 to 6(both inclusive) and returns the choice when found valid. """
    while True:
            choice = input("Choose the option out of above 4 possibilities. Enter 5 to skip, 6 to terminate: ")
            if choice.strip() =="":
                continue
            choice = int(choice)
            if choice>=1 and choice<=6:
                return choice 
                break
            else:
                print("Wrong input. Please re-enter.. ")

def find_all_applications():
    """ scan /usr/share/applications folder and return a dictionary of all applications in the system with mapping of system name to display name. E.g: nautilus: File Explorer. """
    application_path = "/usr/share/applications/"
    files = os.listdir(application_path)
    list_of_applications = {}
    for file in files:
        try:
            file_path = os.path.join(application_path ,file)
            data = subprocess.Popen(["cat", file_path], stdout=subprocess.PIPE)
            grep = subprocess.Popen(
                ["grep", "Application"], stdin=data.stdout, stdout=subprocess.PIPE
            )
            out = grep.communicate()[0].decode("utf-8").strip()
            if out != "":
                data = subprocess.Popen(["cat", file_path], stdout=subprocess.PIPE)
                name_pipe = subprocess.Popen(
                    ["grep", "Name="], stdin=data.stdout, stdout=subprocess.PIPE
                )
                name = (
                    name_pipe.communicate()[0].decode("utf-8").strip().splitlines()[0]
                )
                list_of_applications[file[:-8]]=name[5:]
        except:
            pass

    return list_of_applications


def firefox_history_scan(categorised_data):
    """ Scan the sqlite file of firefox history in the PC and add all visited URLs along with their visit count to browser_history_log.json. This will be used to request the user for categorize the most visited yet unresolved domains in the browser."""
    prev_data = {}
    # try:
    #     prev_data = json.load(open(file_name, "r"))
    # except:
    #     pass
    data_path = os.path.expanduser("~") + "/.mozilla/firefox/*.default*/"
    all_possible_paths = glob.glob(data_path)
    location = "places.sqlite"
    history_path = [x + location for x in all_possible_paths]
    for i in range(len(history_path)):
        if os.path.exists(history_path[i]): # if a db file exists
            # make a copy of it to remove lock and prevent any unwanted errors.
            os.system('cp {} {}'.format(history_path[i], os.path.join(all_possible_paths[i],"places.backup.sqlite")))
            # Save the path to backup file to be used later
            path = os.path.join(all_possible_paths[i],'places.backup.sqlite')
            if os.path.exists(path): # if the backup file was made successfully....
                try:
                    c = sqlite3.connect(path)
                    cursor = c.cursor()

                    select_statement = (
                        "select moz_places.url, moz_places.visit_count from moz_places;"
                    )
                    cursor.execute(select_statement)
                    results = cursor.fetchall()

                    for url, count in results:
                        url_object = tldextract.extract(url)
                        subdomain = (
                            url_object.subdomain + "."
                            if url_object.subdomain.strip() != ""
                            else ""
                        )
                        domain = (
                            url_object.domain + "." if url_object.domain.strip() != "" else ""
                        )
                        suffix = url_object.suffix if url_object.suffix.strip() != "" else ""
                        main_url = "{}{}{}".format(subdomain, domain, suffix)
                        domain = url_object.domain
                        if domain.strip() != "":
                            domain = domain.lower()
                            if categorised_data["website"].get(domain)==None: # domain is not yet categorised
                                prev_data["website"][domain] = prev_data.get(domain, dict())
                                prev_data["website"][domain]["site"] = prev_data[domain].get("site", list())
                                if main_url not in prev_data["website"][domain]["site"]:
                                    prev_data["website"][domain]["site"].append(main_url)
                                    prev_data["website"][domain]["count"] = (
                                        prev_data["website"][domain].get("count", 0) + count
                                    )
                    
                    # Now remove the backup file after the work is complete
                    try:
                        os.system('rm {}'.format(path))
                    except:
                        pass

                except Exception as e:
                    print("ERROR", e)
                    print()
                    pass


    return prev_data

if __name__ == "__main__":
    main()
    # data_dic = firefox_history_scan()

    # pprint.pprint(data_dic)
    # Sort the data_dic as per count
