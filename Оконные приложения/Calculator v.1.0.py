#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import tkinter.ttk
from tkinter import *
from tkinter import messagebox

root = tkinter.Tk()
root.title('Calculator')
root.resizable(False, False)

# логика калькулятора
def calc(key):
    global memory
    if key == '=':              # проверка на вводимые данные
        strl = '-+0123456789*/'
        if calc_entry.get()[0] not in strl:                         # .get() считывает вводимое
            calc_entry.insert(END, ' Ошибка №1')                   # .insert() вводин написаное END- это позиция в поле
            messagebox.showinfo('Ошибка №1')
# счёт
        try:                    # проверка на соответствие логике калькулятора
            result = eval(calc_entry.get())
            calc_entry.insert(END, '=' + str(result))
        except:
            calc_entry.insert(END, ' Ошибка №2')
            messagebox.showinfo('Ошибка №2')

# очистка поля
    elif key == 'C':
        calc_entry.delete(0, END)
# вывод данных
    else:
        if '=' in calc_entry.get():
            calc_entry.delete(0, END)
        calc_entry.insert(END, key)



# создание кнопок
bttn_list = [
    '7', '8', '9', '+', '-',
    '4', '5', '6', '*', '/',
    '1', '2', '3', '=', '',
    '', '0', 'C', '', ''
]

r = 1
c = 0
# цикл создает все кнопки
for i in bttn_list:
    rel = ''
    # значение каждой нажатой кнопки передается в calc()
    cmd = lambda x=i: calc(x)
    ttk.Button(root, text=i, command=cmd).grid(row=r, column=c)         # команда у кнопки cmd
    # разметка
    c += 1
    if c > 4:
        c = 0
        r += 1

# создание поля для ввода

calc_entry = Entry(root, width=33)
calc_entry.grid(row=0, column=0, columnspan=5)


root.mainloop()

