#!/usr/bin/env/python3
# -*- coding: utf-8 -*-


import tkinter.ttk
from tkinter import *
from tkinter import messagebox
import random


def ran():
    global a
    a = random.randint(1, 101)
    btn_2['state'] = 'disabled'
    label_3['text'] = 'Число сгенерировано'
    label_2['text'] = ''
    calc_entry.delete(0, END)


def go():
    try:
        if int(calc_entry.get()) == a:
            label_2['text'] = 'Вы победили!'
            messagebox.showinfo('Результат', 'Вы победили')
            btn_2['state'] = 'normal'
        elif int(calc_entry.get()) != a:
            if int(calc_entry.get()) > a:
                label_2['text'] = str(calc_entry.get()) + ' не верно! Попробуй число меньше'
                calc_entry.delete(0, END)
            elif int(calc_entry.get()) < a:
                label_2['text'] = str(calc_entry.get()) + ' не верно! Попробуй число больше'
                calc_entry.delete(0, END)
    except:
        calc_entry.delete(0, END)
        messagebox.showinfo('Ошибка', 'В поле должно быть число')


root = tkinter.Tk()
root.title('Game: Guess one number of 100')
root.resizable(False, False)
root.geometry('530x300')

text_1 = 'Сгенерировать число:\n\n\nПопробуй отгадать: '
label_1 = Label(text=text_1, justify=LEFT, font='Arial 11')
label_1.place(relx=.05, rely=.01)

calc_entry = Entry(root, width=35)
calc_entry.place(relx=.34, rely=.195)

btn_1 = Button(
    text='Попробывать',
    padx='1',
    pady='1',
    font='1',
    background="#666",
    foreground="#fff",
    # state='disabled'
    state='normal'
)

btn_1['command'] = go
btn_1.place(relx=.87, rely=.285, anchor="s")

btn_2 = Button(
    text='Сгенерировать',
    padx='1',
    pady='1',
    font='1',
    background="#666",
    foreground="#fff",
    state='normal'
)

btn_2['command'] = ran
btn_2.place(relx=.48, rely=.12, anchor="s")

label_2 = Label(text='', justify=LEFT, font='Arial 11')
label_2.place(relx=.31, rely=.45)

label_3 = Label(text='', justify=LEFT, font='Arial 11')
label_3.place(relx=.64, rely=.03)

btn_3 = Button(
    text='Выход',
    padx='1',
    pady='1',
    font='1',
    background="#666",
    foreground="#fff",
    state='normal'
)

btn_3['command'] = root.destroy
btn_3.place(relx=.08, rely=.97, anchor="s")

root.mainloop()
