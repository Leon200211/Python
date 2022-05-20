import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import matplotlib.pyplot as plt
import numpy as np
import re

now = datetime.datetime.now()



def corona_1():
    info_corona = ""
    page = requests.get("https://coronavirusstat.ru/country/russia/")
    soup = BeautifulSoup(page.text, "html.parser")
    mas = []
    mas_2 = []
    result = soup.findAll("div", {"class":"row justify-content-md-center"})
    mas.append(str(result[0].find("div", {"title":"Короновирус Россия: Случаев"}).find("b").text)[:-5].replace(",", "."))
    mas.append(str(result[0].find("div", {"title":"Короновирус Россия: Активных"}).find("b").text)[:-5].replace(",", "."))
    mas.append(str(result[0].find("div", {"title":"Короновирус Россия: Вылечено"}).find("b").text)[:-5].replace(",", "."))
    mas.append(str(result[0].find("div", {"title":"Короновирус Россия: Умерло"}).find("b").text)[:-5].replace(",", "."))
    result = soup.findAll("span", {"class":"text-muted"})
    for i in range(len(result)):
        if(str(result[i].text)[1:].isdigit()):
            mas_2.append(int(result[i].text))
    mas[0] = float(mas[0])*1000000
    mas[1] = float(mas[1])*1000
    mas[2] = float(mas[2])*1000000
    mas[3] = float(mas[3])*1000

    if(int(now.day)<10):
        day = "0"+str(now.day)
    else:
        day = str(now.day)

    if(int(now.month)<10):
        month = "0"+str(now.month)
    else:
        month = str(now.month)
    info_corona += "По состоянию на " + day +  "." + month + "\n"
    info_corona += "Случаев: " + str(mas[0]) + " (" + str(mas_2[0]) + " за сегодня)" + "\n"
    info_corona += "Активных: " + str(mas[1]) + " (" + str(mas_2[1]) + " за сегодня)" + "\n"
    info_corona += "Вылечено: " + str(mas[2]) + " (" + str(mas_2[2]) + " за сегодня)" + "\n"
    info_corona += "Умерло: " + str(mas[3]) + " (" + str(mas_2[3]) + " за сегодня)" + "\n"

    mas = []
    mas_1 = []
    mas_2 = []
    mas_3 = []
    mas_th = []
    result = soup.find("table", {"class":"table table-bordered small"}).find_all("th")
    for i in range(5,len(result)-5):
        mas_th.append(result[i].text[:-5])
    result = soup.find("table", {"class":"table table-bordered small"}).find_all("td")
    print(result)
    count_1 = 1
    for i in range(len(result)-20):
        if(count_1 == 4):
            count_1 = 1
        else:
            mas.append(str(result[i].text))
            count_1 += 1
    for i in range(len(mas)):
        mas[i] = mas[i][1:]
        mas[i] = mas[i][:mas[i].find(" ")]
    for i in range(0,len(mas),3):
        mas_1.append(int(mas[i]))
    for i in range(1,len(mas),3):
        mas_2.append(int(mas[i]))
    for i in range(2,len(mas),3):
        mas_3.append(int(mas[i]))
    print(mas_th)
    mas_th = list(reversed(mas_th))
    print(mas_th)
    # Plot x-labels, y-label and data
    plt.plot([], [], color ='blue',
         label ='Активных')
    plt.plot([], [], color ='orange',
         label ='Вылечено')
    plt.plot([], [], color ='brown',
         label ='Умерло')
    # Implementing stackplot on data
    plt.stackplot(mas_th, mas_1, mas_2,
              mas_3, baseline ='zero',
              colors =['blue', 'orange',
                       'brown'])
    plt.xticks(rotation='45')
    plt.legend()
    plt.title('Россия - детальная статистика - коронавируса')
    fig1 = plt.gcf()
    #plt.show()
    plt.draw()
    fig1.savefig('tessstttyyy.png', dpi=100)


    return info_corona






def corona_2(msg_from_vk):
    info_corona = ""
    page = requests.get("https://coronavirusstat.ru")
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.findAll("div", {"class":"row border border-bottom-0 c_search_row"})
    #print(result)
    activ = 0
    dead = 0
    for i in range(len(result)):
        #print(result[i].find("span", {"class":"small"}).text)
        if((result[i].find("span", {"class":"small"}).text.lower()).find(msg_from_vk)!=-1):
            region = (result[i].find("a").text)
            mas = (result[i].find_all("div", {"class":"p-1 col-4 col-sm-2"}))
            activ = (result[i].find("div", {"class":"p-1 col-4 col-sm-3"}).text)
            dead = (result[i].find("div", {"class":"p-1 col-3 col-sm-2 d-none d-sm-block"}).text)
    mas[0] = (mas[0].find("div", {"class":"h6 m-0"}).text)[:-11]
    mas[0] = re.sub("^\s+|\n|\r|\t|\s+$", '', mas[0])
    mas[0] = mas[0][:-1]
    mas[1] =  (mas[1].find("div", {"class":"h6 m-0"}).text)[:-6]
    mas[1] = re.sub("^\s+|\n|\r|\s+$", '', mas[1])
    print(mas)
    activ = re.sub("^\s+|\n|\r|\t|\s+$", '', activ)
    for i in range(len(activ)):
        if(activ[i]=="+"or activ[i]=="-"):
            activ = activ[:i]
            break
    activ = re.sub('\D', '', activ)
    dead = re.sub("^\s+|\n|\r|\t|\s+$", '', dead)
    for i in range(len(dead)):
        if(dead[i]=="+"or dead[i]=="-"):
            dead = dead[:i]
            break
    dead = re.sub('\D', '', dead)
    if(int(now.day)<10):
        day = "0"+str(now.day)
    else:
        day = str(now.day)
    if(int(now.month)<10):
        month = "0"+str(now.month)
    else:
        month = str(now.month)
    info_corona += "По состоянию на " + day +  "." + month + "\n"
    info_corona += "Регион: " + str(region) +"\n"
    info_corona += "Случаев: " + str(mas[0]) + "\n"
    info_corona += "Активных: " + str(activ) + "\n"
    info_corona += "Вылечено: " + str(mas[1]) + "\n"
    info_corona += "Умерло: " + str(dead) + "\n"
    print(info_corona)
    return info_corona
#corona_2("москва")
#result = soup.findAll("div", {"class":"row border border-bottom-0 c_search_row"})
#result = soup.find("div").find("Москва").find_parent("div").find_parent("div")
