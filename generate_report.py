#! /usr/bin/env python

import json
from datetime import date, timedelta, datetime
import jinja2
import pdfkit 
# from xhtml2pdf import pisa
import urllib
import matplotlib.pyplot as plt
from config import REPORTS_PATH, TIMER_PATH, TODO_FILE
""" sudo apt-get install wkhtmltopdf """

today_date = date.today().strftime("%d-%m-%Y")


def read_data(MY_PATH):
    try:
        data = json.load(open(MY_PATH, "r"))
    except:
        data = {}
    return data


def write_data(MY_PATH, data):
    json.dump(data, open(MY_PATH, "w+"))


def make_pie_plot(file_name, data):
    """  Given data dictionary, create a pie chart and save it in file_name.png"""
    
    # Tasks = [300,500,700]
    Tasks = list(data.values())
    # my_labels = 'Tasks Pending','Tasks Ongoing','Tasks Completed'
    my_labels = list(data.keys())
    my_colors = ['lightblue','lightsteelblue','silver', 'red', 'green'][-len(Tasks):]
    if len(Tasks)==5:
        my_explode = (0.1, 0.1, 0.1, 0.1, 0.1)
    else: 
        my_explode = (0.1,0)
    fig = plt.figure(figsize =(4, 4), dpi=100)
    fig = plt.figure()
    plt.pie(Tasks, labels=my_labels, autopct='%1.1f%%', startangle=0, shadow = False,colors=my_colors, explode=my_explode,textprops={'fontsize': 14})
    # plt.title('My Tasks')
    plt.axis('equal')
    plt.savefig(file_name, bbox_inches='tight')

def make_line_chart(file_name, data):
    data.reverse()
    Year = [x[0][:-5] for x in data]
    Unemployment_Rate = [x[1] for x in data]
    
    fig = plt.figure(figsize =(10, 6), dpi=100)
    plt.plot(Year, Unemployment_Rate, color='red', marker='o')
    # plt.title('Unemployment Rate Vs Year', fontsize=14)
    plt.xlabel('Days', fontsize=14)
    plt.xticks(rotation= 30)
    plt.ylabel('Total Activity(mins)', fontsize=14)
    plt.grid(True)
    plt.savefig(file_name, bbox_inches='tight')

def make_2_subplots(file_name, data):
    data.reverse()
    x = [x[0][:-5] for x in data]
    y1 = [x[1][0] for x in data]
    y2 = [x[1][1] for x in data]
    fig = plt.figure(figsize=(50,25), dpi=100)
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.tight_layout()
    ax1.plot(x, y1,'-g' ,label = 'Completed')
    plt.grid(True)
    ax2.plot(x , y2,'-r', label = 'Incompleted')
    plt.grid(True)
    fig.autofmt_xdate()
    plt.xticks(rotation= 30)
    plt.tick_params(axis='x', which='major', labelsize=10)
    fig.legend(loc="upper right")

    plt.savefig(file_name, bbox_inches='tight')
    

def check_report_status(data):
    """ Read data from REPORTS_PATH and check if any report was created withing last 15 days. """
    if data == {} or data.get("last_report", None) == None:  # File empty i.e. installation time run
        data["last_report"] = today_date
        write_data(REPORTS_PATH, data)
        return False  # no need to create report
    else:
        today = datetime.today()
        last_report_date = datetime.strptime(data["last_report"], "%d-%m-%Y")
        if (today - last_report_date) / timedelta(days=1) < 5:
            return False
        else:
            return True  # create report


def generate_report(report_data):
    """ Generate report of past 15 days by collecting data from timer.json and todo.json """
    timer_data = read_data(TIMER_PATH)
    todo_data = read_data(TODO_FILE)
    
    today = datetime.today().date()
    today = today - timedelta(days=1)
    last_report_date = datetime.strptime(data["last_report"], "%d-%m-%Y").date()

    timer_datapoints=[]
    acad, nonacad, entert, misc, unknwn, maxacad, maxent = [0]*7
    minacad, minent = [1440] * 2  
    # Iterate over timer_data from today till last_report_date+1
    while today != last_report_date:
        formated_today = datetime.strftime(today, "%d-%m-%Y")
        if timer_data.get(formated_today) !=None:
            # Take aggregation 
            v1 =  timer_data[formated_today]["1"]
            v3 = timer_data[formated_today]["3"]

            acad += v1
            nonacad += timer_data[formated_today]["2"]
            entert += v3
            misc += timer_data[formated_today]["4"]
            unknwn += timer_data[formated_today]["uncategorised"]
            # Find max/minacad and max/minent
            if maxacad <  v1:
                maxacad = v1
            if maxent <  v3:
                maxent = v3
            if minacad > v1:
                minacad = v1
            if minent > v3:
                minent = v3

            timer_datapoints.append([formated_today, sum([v1, timer_data[formated_today]["2"], v3, timer_data[formated_today]["4"], timer_data[formated_today]["uncategorised"]])])
        today = today - timedelta(days=1)

    activity_dict = {"academic":acad, "non-academic":nonacad, "entertainment":entert, "miscalleneous": misc, "unknown":unknwn}
    make_pie_plot("pie1.png", activity_dict)
    make_line_chart("chart1.png", timer_datapoints)

    today = datetime.today().date()
    today = today - timedelta(days=1)
    todo_datapoints=[] 
    compl, incomplt, maxcom, maxincom = [0]*4
    # Iterate over timer_data from today till last_report_date+1
    while today != last_report_date:
        formated_today = datetime.strftime(today, "%d-%m-%Y")
        if todo_data.get(formated_today) !=None and type(todo_data[formated_today][0])==int: # data of type [3,7]
            # Aggregation 
            compl += todo_data[formated_today][0]
            incomplt += todo_data[formated_today][1]
            # Take averages
            if maxcom < todo_data[formated_today][0] :
                maxcom = todo_data[formated_today][0]
            if maxincom < todo_data[formated_today][1] :
                maxincom = todo_data[formated_today][1]

            todo_datapoints.append([formated_today, todo_data[formated_today]])
        today = today - timedelta(days=1)

    todo_dict = {"completed": compl, "incomplete" : incomplt}
    make_pie_plot("pie2.png", todo_dict)
    make_2_subplots("chart2.png",todo_datapoints)

    suggestions=["BlaBla", "BlaBla2", "BlaBla3"]

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "report_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    
    outputText = template.render(today_date=today_date, days=len(timer_datapoints), activity=activity_dict,max_acad=maxacad, max_ent=maxent, min_acad=minacad, min_ent=minent, todo = todo_dict, max_comp_task=maxcom, max_incomp_task=maxincom, suggestions=suggestions , graph_url1 = "/home/raj/Documents/scheduler/pie1.png",graph_url2 = "/home/raj/Documents/scheduler/pie2.png", graph_url3="/home/raj/Documents/scheduler/chart1.png" , graph_url4="/home/raj/Documents/scheduler/chart2.png" )

    html_file = open( "testing.html", 'w')
    html_file.write(outputText)
    html_file.close()
    # HtmlFile = open('/home/raj/Documents/scheduler/testing.html', 'r', encoding='utf-8')
    # source_code = HtmlFile.read() 
    # convert_html_to_pdf(source_code, "testing_report.pdf")
    options = {
        'page-size': 'a4',
        # 'margin-top': '0.9in',
        # 'margin-right': '0.9in',
        # 'margin-bottom': '0.9in',
        # 'margin-left': '0.9in',
        'encoding': "UTF-8",
        # 'footer-line':'',
        # 'footer-font-size':'7',
        # 'footer-right': '[page] of [topage]',
        # 'header-center': 'YOUR HEADER',
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
        # 'no-outline':None
        }
    pdfkit.from_file('/home/raj/Documents/scheduler/testing.html', 'testing_report.pdf', options=options) 
    return 

    


if __name__ == "__main__":
    data = read_data(REPORTS_PATH)
    if check_report_status(data) == True:
        generate_report(data)
