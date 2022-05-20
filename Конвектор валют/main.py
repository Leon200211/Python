#!/usr/bin/env/python3
# -*- coding: utf-8 -*-


import tkinter.ttk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import random
from tkinter.ttk import Notebook, Frame

from parsing import *

import urllib.request
import xml.dom.minidom
from xml.etree import ElementTree
import datetime
import calendar
now = datetime.datetime.now()
from datetime import datetime, timedelta, date
import re

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates




def monthToNum(shortMonth):

    return {
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9,
        'October' : 10,
        'November' : 11,
        'December' : 12
    }[shortMonth]


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    monday = datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday, monday + timedelta(days=6.9)


def fun_1():

    if(combo_2.get()==combo_1.get()):
        label_1['text'] = str(float(calc_entry.get()))
        return


    g = now.month
    if(now.month<10):
        g = "0"+str(now.month)





    respons = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=0"+str(now.day)+"/"+str(g)+"/"+str(now.year))

    dom = ElementTree.parse(respons)

    courses = dom.findall('Valute')

    if(combo_1.get()=="РУБЛЬ"):
        for c in courses:
            if (c.find('Name').text == combo_2.get()):
                value_1 = c.find('Value').text
                nominal = c.find('Nominal').text
        value_1 = value_1.replace(',', '.')
        gf = (int(nominal) / (float(value_1)))
        label_1['text'] = str((float(calc_entry.get()) * gf))
        return
    if(combo_2.get()=="РУБЛЬ"):
        for c in courses:
            if (c.find('Name').text == combo_1.get()):
                value_1 = c.find('Value').text
                nominal = c.find('Nominal').text
        value_1 = value_1.replace(',', '.')
        gf = (int(nominal)/(float(value_1)))
        label_1['text'] = str(float(calc_entry.get())/gf)
        return

    for c in courses:
        if(c.find('Name').text==combo_1.get()):
            value_1 = c.find('Value').text
            nominal_1 = c.find('Nominal').text

    for c in courses:
        if(c.find('Name').text==combo_2.get()):
            value_2 = c.find('Value').text
            nominal_2 = c.find('Nominal').text


    value_1 = value_1.replace(',', '.')
    value_2 = value_2.replace(',', '.')

    gf_1 = (int(nominal_1) / (float(value_1)))
    gf_2 = (int(nominal_2) / (float(value_2)))
    print(gf_1,gf_2)
    label_1['text'] = str(((float(calc_entry.get())/gf_1)/float(value_2)))
    #calc_entry.delete(0, END) очищение поля

    btn_1['state'] = 'normal'


def select():
    level = radio_state.get()

    if(level==1):

        mas = []

        week = datetime.now().isocalendar()[1]
        now_week = get_start_and_end_date_from_calendar_week(now.year, week)
        mas.append(now_week)
        week-=1
        now_week = get_start_and_end_date_from_calendar_week(now.year, week)
        mas.append(now_week)
        week-=1
        now_week = get_start_and_end_date_from_calendar_week(now.year, week)
        mas.append(now_week)
        week-=1
        now_week = get_start_and_end_date_from_calendar_week(now.year, week)
        mas.append(now_week)
        combo_4["values"] = mas

    elif(level==2):
        combo_4["values"] = [calendar.month_name[now.month]+" "+str(now.year),calendar.month_name[now.month-1]+" "+str(now.year),calendar.month_name[now.month-2]+" "+str(now.year),calendar.month_name[now.month-3]+" "+str(now.year)]

    elif(level==3):

        mas = []

        last_month = now.month
        start_month = now.month-2
        if(start_month<=0):
            start_month+=12

        mas.append(str(calendar.month_name[start_month]+" - "+calendar.month_name[last_month]))

        last_month=start_month-1
        start_month=last_month-2
        if(start_month<=0):
            start_month+=12
        mas.append(str(calendar.month_name[start_month]+" - "+calendar.month_name[last_month]))

        last_month=start_month-1
        start_month=last_month-2
        if(start_month<=0):
            start_month+=12
        mas.append(str(calendar.month_name[start_month]+" - "+calendar.month_name[last_month]))

        last_month=start_month-1
        start_month=last_month-2
        if(start_month<=0):
            start_month+=12
        mas.append(str(calendar.month_name[start_month]+" - "+calendar.month_name[last_month]))

        combo_4["values"] = mas

    elif(level==4):
        combo_4["values"] = [now.year, now.year-1,now.year-2,now.year-3]



def creat():
    valute = combo_3.get()
    period = combo_4.get()

    if(len(str(period)) == 4):
        period_1 = int(period)
        mas_1, mas_2 = parsing_year(period_1, valute)
        matplotlib.use("TkAgg")
        fig = plt.figure()
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        if(len(mas_1)!=len(mas_2)):
            mas_2 = mas_2[:len(mas_1)]
        plt.plot(mas_2, mas_1)
        plt.xticks(rotation='45')
        plt.grid()
        plot_widget.grid(ipady=100,row=0,column=0, padx=500, pady=155)
        return


    if(any(map(str.isdigit, period))==False):
        start_month = ""
        end_month = ""
        textlookfor = r"[A-Z][a-z]+"
        allres = re.findall(textlookfor, period)

        start_month=allres[0]
        end_month=allres[1]
        start_month = monthToNum(start_month)
        end_month = monthToNum(end_month)

        mas_1, mas_2 = parsing_kvartal(start_month, end_month,valute)
        matplotlib.use("TkAgg")
        fig = plt.figure()
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        if(len(mas_1)!=len(mas_2)):
            mas_2 = mas_2[:len(mas_1)]
        plt.plot(mas_2, mas_1)
        plt.grid()
        plot_widget.grid(ipady=100,row=0,column=0, padx=500, pady=155)
        return

    if(re.search(r'[A-Z]', period)!=None):
        our_month = ""
        for i in range(len(period)):
            if(period[i]==" "):
                break
            our_month = our_month + str(period[i])


        mas_1, mas_2 = parsing_month(monthToNum(our_month), valute)
        fig = plt.figure()
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        if(len(mas_1)!=len(mas_2)):
            mas_2 = mas_2[:len(mas_1)]
        plt.plot(mas_2, mas_1)
        plt.xticks(rotation='45')
        plt.grid()

        plot_widget.grid(ipady=100,row=0,column=0, padx=500, pady=155)
        return


    mas_1,mas_2  = (parsing_week(period, valute))
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
    plot_widget = canvas.get_tk_widget()
    fig.clear()
    if(len(mas_1)!=len(mas_2)):
        mas_2 = mas_2[:len(mas_1)]
    plt.plot(mas_1, mas_2)
    plt.xticks(rotation='45')
    plt.grid()
    plot_widget.grid(ipady=100,row=0,column=0, padx=500, pady=155)
    return


    #print(parsing_year(2020, "Азербайджанский манат"))


root = tkinter.Tk()
root.title('Конвертер валют')
root.resizable(False, False)
root.geometry('1500x900')




tab_control = Notebook(root)
tab1 = Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab2 = Frame(tab_control)
tab_control.add(tab2, text="Динамика курса")
tab_control.pack(expand = 1, fill = "both")

# список один
mas_for_one = parsing()
mas_for_one.append("РУБЛЬ")
combo_1 = ttk.Combobox(tab1)
combo_1["values"] = mas_for_one
combo_1.grid(column=0, row=0)
combo_1.place(relx=.008, rely=.02)
# список два
combo_2 = ttk.Combobox(tab1)
combo_2["values"] = mas_for_one
combo_2.grid(column=0, row=0)
combo_2.place(relx=.008, rely=.08)
# ввод количества
calc_entry = Entry(tab1, width=35)
calc_entry.place(relx=.15, rely=.02)
# вывод результата
label_1 = Label(tab1,text='', justify=LEFT, font='Arial 11')
label_1.place(relx=.15, rely=.08)
# кнопка
btn_1 = Button(
    tab1,
    text='Конвертировать',
    padx='0.5',
    pady='0.5',
    font='0.5',
    background="#666",
    foreground="#fff",
    state='normal'
)

btn_1['command'] = fun_1
btn_1.place(relx=.38, rely=.05, anchor="s")




# ===================================вторая вкладка===================================

text_2 = 'Валюты'
label_2 = Label(tab2, text=text_2, justify=LEFT, font='Arial 11')
label_2.place(relx=.03, rely=.02)

combo_3 = ttk.Combobox(tab2)
combo_3["values"] = parsing()
combo_3.grid(column=0, row=0)
combo_3.place(relx=.01, rely=.05)

text_3 = 'Период'
label_3 = Label(tab2, text=text_3, justify=LEFT, font='Arial 11')
label_3.place(relx=.15, rely=.02)

text_4 = 'Выбор периода'
label_4 = Label(tab2, text=text_4, justify=LEFT, font='Arial 11')
label_4.place(relx=.25, rely=.02)

combo_4 = ttk.Combobox(tab2)
combo_4["values"] = [1,2,3]
combo_4.grid(column=0, row=0)
combo_4.place(relx=.24, rely=.06)

radio_state = IntVar()
radio_state.set(4)
radiobutton1 = Radiobutton(tab2, text = "Неделя",value = 1, variable = radio_state, command=select)
radiobutton1.grid(row = 1, column = 1)
radiobutton1.place(relx=.14, rely=.06)

radiobutton2 = Radiobutton(tab2, text = "Месяц",value = 2, variable = radio_state, command=select)
radiobutton2.grid(row = 2, column = 1)
radiobutton2.place(relx=.14, rely=.09)

radiobutton3 = Radiobutton(tab2, text = "Квартал",value = 3, variable = radio_state, command=select)
radiobutton3.grid(row = 3, column = 1)
radiobutton3.place(relx=.14, rely=.12)

radiobutton3 = Radiobutton(tab2, text = "Год",value = 4, variable = radio_state, command=select)
radiobutton3.grid(row = 4, column = 1)
radiobutton3.place(relx=.14, rely=.15)





btn_2 = Button(
    tab2,
    text='Построить график',
    padx='0.5',
    pady='0.5',
    font='0.5',
    background="#666",
    foreground="#fff",
    state='normal'
)

btn_2['command'] = creat
btn_2.place(relx=.055, rely=.2, anchor="s")


root.mainloop()


