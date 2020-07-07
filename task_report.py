#! /usr/bin/env python

""" Program to iterate last 7 data of toDo completition and generate and display a bar chart representing that data """

import os
import json
from datetime import date, timedelta 
from matplotlib import pyplot as plt
from PIL import Image
import operator
import numpy as np 
from config import TODO_FILE, SAVE_PATH


def generate_graph(data_dict):
    """ Function to take list of dates along with corresponding completed and incompleted tasks count and represent them in a stacked bar chart. """
    # data_dict = sorted(data_dict.items())
    dates, cmplt_lst, incmplt_lst= [], [],[]
    for item in data_dict:
        k,v = item[0], item[1]
        dates.append(k)
        cmplt_lst.append(v[0])
        incmplt_lst.append(v[1])

    fig, ax = plt.subplots()
    index = np.arange(len(dates))
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, cmplt_lst, bar_width,
    alpha=opacity,
    color='xkcd:electric blue',
    label='Complete tasks', edgecolor="black")

    rects2 = plt.bar(index + bar_width, incmplt_lst, bar_width,
    alpha=opacity,
    color='r',
    label='Incomplete tasks', edgecolor="black")
    # fig = plt.figure(figsize=(10,7))
    plt.xlabel('Dates', fontsize=14)
    plt.ylabel('Weight', fontsize=14)
    plt.title('Consistency plot', fontsize=20)
    plt.yticks(np.arange(1, max(max(cmplt_lst),max(incmplt_lst)) + 3, 1))
    plt.xticks(index + bar_width/2, dates)
    plt.legend()

    plt.tight_layout()
    # plt.show()
    today_date = date.today().strftime("%d-%m-%Y")
    
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    plt.savefig( SAVE_PATH+str(today_date)+".png", bbox_inches='tight')
    # print("Saved the report successfully")
    try:
        img = Image.open(SAVE_PATH+str(today_date)+".png")
        img.show()
        # print("Image display successful")
    except Exception as e:
        print(e)

def get_data():
    """ Function to get at most 7 data points from the data file """
    
    today_date = date.today().strftime("%d-%m-%Y")
    # print("Started program at ",today_date )
    data = read_file()
    # get 7 data points or less 
    data_dict = [] # list of all dates in order. [[dd-mm, [3,1]], [dd-mm, [2,6]] ]
    k=0 # number of data points
    for i in range(1,31):
        if k>=7:
            break 
        new_date = (date.today() - timedelta(days=i)).strftime("%d-%m-%Y")
        if data.get(new_date)!=None: 
            # if  type(data[new_date][0])==list:
                # continue
            if type(data[new_date][0])==int: # found a data point
                k+=1
                data_dict.append([new_date[:-5],data[new_date]]) 

    if len(data_dict)!=0:
        data_dict.reverse()
        generate_graph(data_dict)
    # else:
        # print("No data found within 30 days from now.")

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  

if __name__ == "__main__":
    # os.system("clear")
    # message="===========Pending Tasks========="
    get_data()

