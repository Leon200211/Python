#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import tkinter.ttk
from tkinter import *
from tkinter import messagebox
import random
import time

you = 0  # переменный счета
pc = 0
you_figur = ''  # переменные выбора
pc_figut = ''


def stone():  # функция изменения параметров кнопки при нажатии
    global you_figur
    btn_1['bg'] = 'green'
    you_figur = 'Камень'
    btn_5['state'] = 'normal'
    btn_2['state'] = 'disabled'
    btn_3['state'] = 'disabled'
    label_2['text'] = 'Выбор PC - '


def noj():  # функция изменения параметров кнопки при нажатии
    global you_figur
    btn_2['bg'] = 'green'
    you_figur = 'Ножницы'
    btn_5['state'] = 'normal'
    btn_1['state'] = 'disabled'
    btn_3['state'] = 'disabled'
    label_2['text'] = 'Выбор PC - '


def paper():  # функция изменения параметров кнопки при нажатии
    global you_figur
    btn_3['bg'] = 'green'
    you_figur = 'Бумага'
    btn_5['state'] = 'normal'
    btn_1['state'] = 'disabled'
    btn_2['state'] = 'disabled'
    label_2['text'] = 'Выбор PC - '


def go():  # функция определяет победителя
    global you_figur, pc_figut, you, pc
    l = ['Камень', 'Ножницы', 'Бумага']
    pc_figut = random.choice(l)
    label_2['text'] = 'Выбор PC - ' + pc_figut
    time.sleep(0.5)

    if you_figur == pc_figut:
        messagebox.showinfo('Результат', 'Ничья')

    else:
        if you_figur == 'Камень' and pc_figut == 'Бумага':
            pc += 1
            messagebox.showinfo('Результат', 'PC победил')
        elif you_figur == 'Камень' and pc_figut == 'Ножницы':
            you += 1
            messagebox.showinfo('Результат', 'Вы победили')
        elif you_figur == 'Ножницы' and pc_figut == 'Камень':
            pc += 1
            messagebox.showinfo('Результат', 'PC победил')
        elif you_figur == 'Ножницы' and pc_figut == 'Бумага':
            you += 1
            messagebox.showinfo('Результат', 'Вы победили')
        elif you_figur == 'Бумага' and pc_figut == 'Камень':
            you += 1
            messagebox.showinfo('Результат', 'Вы победили')
        elif you_figur == 'Бумага' and pc_figut == 'Ножницы':
            pc += 1
            messagebox.showinfo('Результат', 'PC победил')

        label_3['text'] = 'You - ' + str(you)
        label_4['text'] = 'PC - ' + str(pc)

    btn_5['state'] = 'normal'
    btn_1['state'] = 'normal'
    btn_2['state'] = 'normal'
    btn_3['state'] = 'normal'
    btn_1['bg'] = 'gray'
    btn_2['bg'] = 'gray'
    btn_3['bg'] = 'gray'


# создание окна

root = tkinter.Tk()
root.title('Game')
root.geometry("600x400")
root.resizable(False, False)

# создание кнопок

btn_1 = Button(  # создание перовой кнопки
    text='Камень',
    padx='15',
    pady='8',
    font='12',
    background="#666",
    foreground="#fff",
)

btn_1['command'] = stone
btn_1.place(relx=.2, rely=.3, anchor="s")

btn_2 = Button(
    text='Ножницы',
    padx='15',
    pady='8',
    font='12',
    background="#666",
    foreground="#fff"
)
btn_2['command'] = noj
btn_2.place(relx=.5, rely=.3, anchor="s")

btn_3 = Button(
    text='Бумага',
    padx='15',
    pady='8',
    font='12',
    background="#666",
    foreground="#fff"
)
btn_3['command'] = paper
btn_3.place(relx=.8, rely=.3, anchor="s")

btn_4 = Button(
    text='Выход',
    padx='2',
    pady='2',
    font='2',
    background="#666",
    foreground="#fff"
)
btn_4['command'] = root.destroy
btn_4.place(relx=.07, rely=.97, anchor="s")

btn_5 = Button(
    text='Сгенирировать',
    padx='15',
    pady='8',
    font='12',
    background="#666",
    foreground="#fff",
    state='disabled'
)

btn_5['command'] = go
btn_5.place(relx=.5, rely=.6, anchor="s")

# текс в окне

text_1 = 'Сделайте свой выбор:'
label_1 = Label(text=text_1, justify=LEFT, font='Arial 15')
label_1.place(relx=.33, rely=.07)
label_2 = Label(text='', justify=LEFT, font='Arial 15')
label_2.place(relx=.34, rely=.65)
label_3 = Label(text='You - 0', justify=LEFT, font='Arial 13')
label_3.place(relx=.82, rely=.58)
label_4 = Label(text='PC - 0', justify=LEFT, font='Arial 13')
label_4.place(relx=.82, rely=.63)
text_5 = 'Счёт:'
label_5 = Label(text=text_5, justify=LEFT, font='Arial 14')
label_5.place(relx=.8, rely=.5)
label_6 = Label(text='', justify=LEFT, font='Arial 14')
label_6.place(relx=.38, rely=.75)

root.mainloop()
