import urllib.request
import xml.dom.minidom
from xml.etree import ElementTree
import re
import datetime
import calendar
now = datetime.datetime.now()
from datetime import datetime, timedelta, date

def parsing():
    mas = []
    respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=17/04/2021")

    dom = ElementTree.parse(respons)


    courses = dom.findall('Valute/Name')

    for c in courses:
        mas.append(c.text)

    return mas



def parsing_year(year, name):
    mas = []

    mas_2 = []

    month = 1
    for i in range(1, 13):
        if(i<10):
            s = "01/0"+str(i)+"/"+str(year)
        else:
            s = "01/"+str(i)+"/"+str(year)
        mas_2.append(s)
        respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+s)
        dom = ElementTree.parse(respons)
        courses = dom.findall('Valute')

        for c in courses:
            if(c.find('Name').text==name):
                nominal_1 = c.find('Nominal').text
                gf_1 = float((int(nominal_1)) / float((c.find('Value').text).replace(',', '.')))
                mas.append(gf_1)
                #mas.append(float((c.find('Value').text).replace(',', '.')))


    return mas, mas_2


def parsing_month(month, name):
    mas = []
    mas_2 = []
    day = 1

    new_month = str(month)
    if(int(month)<10):
        new_month = new_month[:0] + "0" + new_month[0:]

    for i in range(1, 32):
        if(i<10):
            s = "0"+str(i)+"/"+str(new_month)+"/2021"
        else:
            s = str(i)+"/"+str(new_month)+"/2021"
        respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+s)
        dom = ElementTree.parse(respons)
        courses = dom.findall('Valute')

        mas_2.append(s)

        for c in courses:
            if(c.find('Name').text==name):
                nominal_1 = c.find('Nominal').text
                gf_1 = float((int(nominal_1)) / float((c.find('Value').text).replace(',', '.')))
                mas.append(gf_1)
                #mas.append(float((c.find('Value').text).replace(',', '.')))


    return mas, mas_2


def parsing_kvartal(month_start,month_end, name):

    mas = []
    mas_2 = []

    mas_1 = []
    mas_1.append(month_start)
    while(month_start!=month_end):
        month_start+=1
        if(month_start>12):
            month_start = 1
        mas_1.append(month_start)

    new_month = ""

    for i in range(len(mas_1)):
        if(mas_1[i]<10):
            new_month = str(mas_1[i])[:0] + "0" + str(mas_1[i])[0:]
            s = "01"+"/"+str(new_month)+"/2020"
        else:
            s = "01"+"/"+str(mas_1[i])+"/2020"
        if(int(mas_1[i])<=now.month):
            new_month = str(mas_1[i])[:0] + "0" + str(mas_1[i])[0:]
            s = "01"+"/"+str(new_month)+"/2021"
            respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+s)
            dom = ElementTree.parse(respons)
            courses = dom.findall('Valute')
            mas_2.append(s)
            for c in courses:
                if(c.find('Name').text==name):
                    mas.append(float((c.find('Value').text).replace(',', '.')))
        else:
            respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+s)
            dom = ElementTree.parse(respons)
            courses = dom.findall('Valute')


            mas_2.append(s)
            for c in courses:
                if(c.find('Name').text==name):
                    nominal_1 = c.find('Nominal').text
                    gf_1 = float((int(nominal_1)) / float((c.find('Value').text).replace(',', '.')))
                    mas.append(gf_1)
                    #mas.append(float((c.find('Value').text).replace(',', '.')))

        if(mas_1[i]<10):
            new_month = str(mas_1[i])[:0] + "0" + str(mas_1[i])[0:]
            s = "15"+"/"+str(new_month)+"/2020"
        else:
            s = "15"+"/"+str(mas_1[i])+"/2020"

        if(int(mas_1[i])<=now.month):
            new_month = str(mas_1[i])[:0] + "0" + str(mas_1[i])[0:]
            s = "15"+"/"+str(new_month)+"/2021"
        respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+s)
        dom = ElementTree.parse(respons)
        courses = dom.findall('Valute')
        mas_2.append(s)
        for c in courses:
            if(c.find('Name').text==name):
                nominal_1 = c.find('Nominal').text
                gf_1 = float((int(nominal_1)) / float((c.find('Value').text).replace(',', '.')))
                mas.append(gf_1)
                #mas.append(float((c.find('Value').text).replace(',', '.')))




    return mas, mas_2


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



def parsing_week(week, name):

    mas = []

    weeks = week.split()
    week_start=weeks[0]
    week_end=weeks[1]

    week_start = week_start.split("-")
    week_end = week_end.split("-")

    week_start=date(int(week_start[0]),int(week_start[1]),int(week_start[2]))
    week_end=date(int(week_end[0]),int(week_end[1]),int(week_end[2]))

    stroka_2 = ""

    for single_date in daterange(week_start, week_end):
        stroka = (single_date.strftime("%Y-%m-%d"))
        stroka = str(stroka)
        stroka = stroka.split("-")

        stroka_3 = []
        for i in reversed(stroka):
            stroka_3.append(i)



        for i in range(len(stroka_3)):
            stroka_2+=str(stroka_3[i])+"-"

        stroka_2 = stroka_2[0:-1]
        mas.append(stroka_2)

        stroka = ""
        stroka_2 = ""
        stroka_3 = ""


    stroka = week_end
    stroka = str(stroka)
    stroka = stroka.split("-")

    stroka_3 = []
    for i in reversed(stroka):
        stroka_3.append(i)


    for i in range(len(stroka_3)):
        stroka_2+=str(stroka_3[i])+"-"


    stroka_2 = stroka_2[0:-1]

    mas.append(str(stroka_2))




    mas_1=[]

    for i in range(len(mas)):
        s = str(mas[i])



        respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+s)
        dom = ElementTree.parse(respons)
        courses = dom.findall('Valute')

        for c in courses:
            if(c.find('Name').text==name):
                nominal_1 = c.find('Nominal').text
                gf_1 = float((int(nominal_1)) / float((c.find('Value').text).replace(',', '.')))
                mas_1.append(gf_1)
                #mas_1.append(float((c.find('Value').text).replace(',', '.')))

    return mas, mas_1


#print(parsing_year("2020", "Азербайджанский манат"))
#print(parsing_month(2, "Азербайджанский манат"))
#print(parsing_kvartal(11,1, "Азербайджанский манат"))
#mas_1,mas_2  = (parsing_week("2021-04-26 2021-05-02", "Азербайджанский манат"))
#print(mas_1)
#print(mas_2)

