from tkinter import *
from tkinter.ttk import Notebook, Frame, Combobox, Checkbutton, Radiobutton
import tkinter.ttk as ttk
from datetime import datetime, date, time
import urllib.request
import xml.dom.minidom
date_today = date.today()
url="http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(date_today.day) + "/0" + str(date_today.month) + "/" + str(date_today.year)
print (url)

def btn1_click():
    j = 0
    for ls in list_1:
        j = j+1
        if (ls == combobox1.get()):
            break
    zn=list_2[j]
    zn = zn.replace(',', '.')
    znach_1=float(zn)
    j = 0
    for l in list_1:
        j = j+1
        if l == combobox2.get():
            break
    zn1=list_2[j]
    zn1 = zn1.replace(',', '.')
    znach_2=float(zn1)
    res = znach_2*int(entry1.get())/znach_1
    label1.configure(text=str(res))
    return 0
response = urllib.request.urlopen(url)
dom = xml.dom.minidom.parse(response)
dom.normalize()
nodeArray=dom.getElementsByTagName("Name")
nodeArray_2=dom.getElementsByTagName("Value")
list_1 = []
list_2 = []
for node in nodeArray:
    childlist=node.childNodes
    for child in childlist:
        list_1.append(child.nodeValue)

for node in nodeArray_2:
    childlist=node.childNodes
    for child in childlist:
        list_2.append(child.nodeValue)
window = Tk()
window.title("Conventor")
window.geometry("450x200")


tab_control = Notebook(window)
tab1 = Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")

tab2 = Frame(tab_control)
tab_control.add(tab2, text="Динамика курса")

combobox1 = Combobox(tab1)
combobox1["values"] = list_1
combobox1.current(3)
combobox1.grid(row = 0, column = 1)

combobox2 = Combobox(tab1)
combobox2["values"] = list_1
combobox2.current(3)
combobox2.grid(row = 2, column = 1, padx=0, pady=15)
tab_control.pack(expand = True, fill = BOTH)

entry1 = Entry(tab1)
entry1.grid(row = 0, column = 2, padx=15, pady=0)


label1 = Label(tab1, text = "0")
label1.grid(column=2, row=2, padx=15)

button1 = Button(tab1, text="Конвертировать", command =
btn1_click)
button1.grid(column=3, row=0, padx=15)

window.mainloop()
