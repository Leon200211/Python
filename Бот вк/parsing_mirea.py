import requests
from bs4 import BeautifulSoup
import openpyxl
import datetime
import pendulum
from translate import Translator

import re

translator= Translator(from_lang="english",to_lang="russian")
now = datetime.datetime.now()

def parsing_prepod(group, vk_msg,when):
    mas_prepod = []
    mas_name_prepod = []
    When = datetime.datetime.today().weekday()
    if(when=="на завтра"):
        When += 1
        print(When)
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day+1).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на сегодня"):
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на эту неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на следующую неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "I"
        else:
            parsing_week = "II"

    link = parsing()
    vk_group = str(group[len(group) - 2])+str(group[len(group) - 1])

    if(vk_group=="20"):
        link_to_fl = link[0]
        parsing_row = 421+10
    elif(vk_group=="19"):
        link_to_fl = link[1]
        parsing_row = 342
    elif(vk_group=="18"):
        link_to_fl = link[2]
        parsing_row = 221

    filename = link_to_fl.split('/')[-1]
    r = requests.get(link_to_fl, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    book = openpyxl.open(filename, read_only=True)
    sheet = book.active

    para_counter = 1



    try:
        for i in range(7, parsing_row, 5):
            para_counter = 1

            """
            try:
                if(len(mas_name_prepod)!= 0):
                    for h in range(len(mas_name_prepod)):
                        mas_prepod[h] += "Расписание у группы: "+ sheet[2][i-2].value + "\n"
                else:
                    mas_prepod.append("Расписание у группы: "+ sheet[2][i-2].value + "\n")
            except TypeError:
                pass
            """

            for j in range(parsing_start, parsing_end):
                print(str(sheet[j][i].value), j ,i)
                if(str(sheet[j][i].value).lower().find(vk_msg)!=-1 and ((str(sheet[j][i].value)[(sheet[j][i].value).lower().find(vk_msg):len(vk_msg)+5 + (sheet[j][i].value).lower().find(vk_msg)]) in mas_name_prepod)==False):
                    #print((str(sheet[j][i].value)[(sheet[j][i].value).find(vk_msg):len(vk_msg)+5 + (sheet[j][i].value).find(vk_msg)]))

                    mas_name_prepod.append(str(sheet[j][i].value)[(sheet[j][i].value).lower().find(vk_msg):len(vk_msg)+5])
                    #mas_name_prepod.append("Расписание у группы: "+ sheet[2][i-2].value + "\n"+str(sheet[j][i].value)[(sheet[j][i].value).lower().find(vk_msg):len(vk_msg)+5])
                for k in range(len(mas_name_prepod)):
                    #print("----------",str(sheet[j][i-3].value), i , j)
                    if(str(sheet[j][i-3].value) == parsing_week):
                        try:
                            #print(str(sheet[j][i].value))
                            if(str(sheet[j][i].value)[str(sheet[j][i].value).lower().find(vk_msg):str(sheet[j][i].value).lower().find(vk_msg)+5+len(vk_msg)]==mas_name_prepod[k]):
                                try:
                                    if((j-4)%12==0):
                                        print(parsing_start, parsing_start-4, (parsing_start-4)%12)
                                        mas_prepod[k] +="\n"
                                    print(re.sub("^\s+|\n|\r|\s+$","",sheet[j][i-2].value) + "\n")
                                    if(para_counter==1):
                                        mas_prepod[k] +=sheet[2][i-2].value+"\n"
                                        para_counter = 0
                                    mas_prepod[k] += re.sub("^\s+|\n|\r|\s+$","",sheet[j][i-2].value) + "\n"
                                except IndexError:
                                    if(para_counter==1):
                                        mas_prepod.append(sheet[2][i-2].value+"\n"+str(sheet[j][i-2].value) + "\n")
                                        para_counter = 0
                            else:
                                try:
                                    if(para_counter==1):
                                        mas_prepod[k] +=sheet[2][i-2].value+"\n"
                                        para_counter = 0
                                    mas_prepod[k] += "----" + "\n"
                                except IndexError:
                                    if(para_counter==1):
                                        mas_prepod.append(sheet[2][i-2].value+"\n"+str(sheet[j][i-2].value) + "\n")
                                        para_counter = 0
                                    mas_prepod.append("----" + "\n")
                        except AttributeError:
                            pass
            print("=======================")
    except IndexError:
        print(123)
        #return "Возможно вы ввели неправильную фамилию"

    print(mas_prepod)
    print(len(mas_prepod[0]))
    #print(mas_name_prepod)

    #return mas_name_prepod,mas_prepod




def parsing_prepod_2(group, vk_msg,when):
    When = datetime.datetime.today().weekday()


    mas_prepod = []
    mas_name_prepod = []

    if(when=="на завтра"):
        When += 1
        print(When)
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day+1).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на сегодня"):
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на эту неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(when=="на следующую неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "I"
        else:
            parsing_week = "II"

    link = parsing()
    vk_group = str(group[len(group) - 2])+str(group[len(group) - 1])

    if(vk_group=="20"):
        link_to_fl = link[0]
        parsing_row = 421
    elif(vk_group=="19"):
        link_to_fl = link[1]
        parsing_row = 342
    elif(vk_group=="18"):
        link_to_fl = link[2]
        parsing_row = 221

    filename = link_to_fl.split('/')[-1]
    r = requests.get(link_to_fl, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    book = openpyxl.open(filename, read_only=True)
    sheet = book.active
    paracount = 1
    mas_info_prepod = []
    vk_msg = vk_msg[6:].lower()
    print(str(sheet[22][17].value))
    for i in range(7, parsing_row, 5):
        for j in range(parsing_start, parsing_end):
            #print(i ,j,str(sheet[j][4].value),str(sheet[j][i].value).lower())
            print(i ,j)
            if(paracount==7):
                paracount = 1
            if(str(sheet[j][4].value) == parsing_week):
                if(len(mas_name_prepod)==0):
                    if(str(sheet[j][i].value).lower().find(vk_msg.lower())!=-1):
                        mas_name_prepod.append(str(sheet[j][i].value).lower()[str(sheet[j][i].value).lower().find(vk_msg.lower()):str(sheet[j][i].value).lower().find(vk_msg)+len(vk_msg)+5])
                        mas_info_prepod.append(["","","","","",""])
                        mas_info_prepod[0][paracount-1] += str(sheet[j][i-2].value) +" " + str(sheet[2][i-2].value)+ " " +str(sheet[j][i+1].value) +" \n"
                elif(str(sheet[j][i].value).lower().find(vk_msg.lower())!=-1):
                    if(str(sheet[j][i].value).lower()[str(sheet[j][i].value).lower().find(vk_msg.lower()):str(sheet[j][i].value).lower().find(vk_msg)+len(vk_msg)+5] in mas_name_prepod):
                        for k in range(len(mas_name_prepod)):
                            print(mas_name_prepod[k])
                            if(str(sheet[j][i].value).lower().find(mas_name_prepod[k])!=-1):
                                mas_info_prepod[k][paracount-1] += str(sheet[j][i-2].value) +" " +str(sheet[2][i-2].value)+ " " +str(sheet[j][i+1].value) +" \n"
                    else:
                        mas_name_prepod.append(str(sheet[j][i].value).lower()[str(sheet[j][i].value).lower().find(vk_msg.lower()):str(sheet[j][i].value).lower().find(vk_msg)+len(vk_msg)+5])
                        mas_info_prepod.append(["","","","","",""])
                        mas_info_prepod[len(mas_info_prepod)-1][paracount-1] += str(sheet[j][i-2].value) +" " +str(sheet[2][i-2].value) +" " + str(sheet[j][i+1].value) +" \n"

                paracount += 1

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #print(mas_info_prepod)
    #print(mas_name_prepod)
    return mas_name_prepod, mas_info_prepod


def save_from_www_and_parsing(group,When, vk_msg):
    if(group =="start"):
        return "Вы не указали группу"
    #vk_msg = "на следующую неделю"
    link = parsing()
    vk_group = str(group[len(group) - 2])+str(group[len(group) - 1])
    print(vk_group)
    parsing_row = 0

    if(vk_group=="21"):
        link_to_fl = link[0]
        parsing_row = 421
    if(vk_group=="20"):
        link_to_fl = link[0]
        parsing_row = 421
    elif(vk_group=="19"):
        link_to_fl = link[1]
        parsing_row = 342
    elif(vk_group=="18"):
        link_to_fl = link[2]
        parsing_row = 221


    parsing_colum = 0
    parsing_start = 0
    parsing_end = 0
    parsing_week = ""
    colum = 0
    info_respisanie = ""
    day_counter = ""
    para_counter = 1
    if(vk_msg=="на завтра"):
        When += 1
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(vk_msg=="на сегодня"):
        if(When == 7):
            When = 0
        parsing_start = (When*12)+4
        parsing_end = (When*12)+16
        print(parsing_start,parsing_end)
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(vk_msg=="на эту неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "II"
        else:
            parsing_week = "I"
    elif(vk_msg=="на следующую неделю"):
        parsing_start = 4
        parsing_end = 76
        if(((datetime.date(2021, now.month, now.day).isocalendar()[1])-5) % 2 == 0):
            parsing_week = "I"
        else:
            parsing_week = "II"







    filename = link_to_fl.split('/')[-1]
    r = requests.get(link_to_fl, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    book = openpyxl.open(filename, read_only=True)
    sheet = book.active
    try:
        for i in range(0, 500):
            if(str(sheet[2][i].value).lower()==group):
                colum = i
                break
    except IndexError:
        return "Возможно вы ввели неправильный номер группы"
    if(vk_msg=="на сегодня" and info_respisanie.find("Расписание на")!=False):
        print(info_respisanie.find("Расписание на"))
        print("1231241249149812-4812-09481284-184-012841284")
        info_respisanie +="Расписание на "+ str(translator.translate(datetime.datetime.today().strftime('%A')))+ "\n"
    for i in range(parsing_start, parsing_end):
        if(str(sheet[i][colum-1].value) == parsing_week):
            if(para_counter==7):
                para_counter = 1
                info_respisanie +="\n"+ "\n"
            if(str(sheet[i][colum].value) != "None"):
                print(re.sub("^\s+|\n|\r|\s+$", '', str(para_counter)+" | "+(str(sheet[i][colum].value) + " | " + str(sheet[i][colum+1].value) + " | " + str(sheet[i][colum+2].value) + " | "+ str(sheet[i][colum+3].value))) + "\n")
                info_respisanie +=re.sub("^\s+|\n|\r|\s+$", '', str(para_counter)+" | "+(str(sheet[i][colum].value) + " | " + str(sheet[i][colum+1].value) + " | " + str(sheet[i][colum+2].value) + " | "+ str(sheet[i][colum+3].value))) + "\n"
            else:
                print(str(para_counter)+" | "+"---")
                info_respisanie += str(para_counter)+" | "+"---" + "\n"
            para_counter += 1
    print("+=================================+")
    print(datetime.date(2021, 5, 26).isocalendar()[1])
    info_respisanie = info_respisanie.replace("None", "--")
    return info_respisanie


def parsing():
    mas_href = []
    page = requests.get("https://www.mirea.ru/schedule/")
    soup = BeautifulSoup(page.text, "html.parser")
    #look = soup.find("div", class_="rasspisanie").find(string = "Институт информационных технологий").find_parent("div").find_parent("div")
    result = soup.find("div", {"class":"rasspisanie"}).find(string = "Институт информационных технологий").find_parent("div").find_parent("div")
    href = 0
    for i in result.find_all('a', href=True):
        if(href>0 and href<4):
            mas_href.append(i['href'])
        href+=1
    return mas_href


#print(parsing())

#link = parsing()
#print(link)
#save_from_www_and_parsing('икбо-23-20',datetime.datetime.today().weekday(),"на завтра")

#parsing_prepod_2("икбо-23-20", "найти Гаврилова", "на сегодня")

"""
mass = [["",""], ["",""], [""]]
print(mass)
print(len(mass))
"""

"""
print(link)
filename = link[0].split('/')[-1]
r = requests.get(link[0], allow_redirects=True)
open(filename, 'wb').write(r.content)
book = openpyxl.open(filename, read_only=True)
sheet = book.active

colum = 0

for i in range(0, 422):
    if(str(sheet[2][i].value).lower()=="икбо-23-20"):
        colum = i
        break


ab= str(sheet[41][colum].value)
print(ab)

print(re.sub("^\s+|\n|\r|\s+$", '', ab))
"""

#parsing_prepod("икбо-23-20", "найти Гаврилова", "на завтра")