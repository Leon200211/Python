import random
import re
import sys
from itertools import groupby
from prettytable import PrettyTable
import graphviz as gr
import os
import requests
from bs4 import BeautifulSoup


def task1(list1, list2, list3, list4, val, list5, list6):
    print('1 - ', [int(x) for x in list1])
    print('2 - ', len(set(list2)))
    print('3 - ', list3[::-1])
    print('4 - ', [i for i, v in enumerate(list4) if v == val])
    print('5 - ', sum([x for i, x in enumerate(list5) if i % 2 == 0]))
    print('6 - ', max(list6, key=len))


list1 = ["43", "65", "1", "87", "984", "315"]
list2 = [423, 66, 87, 23, 55, 3, 55]
list3 = [78, 545, 77, 99, 44]
list4 = [54, 4334, 54, 113, 54, 87, 54, 323]
val = 54
list5 = [21, 55, 44, 43, 78, 10, 94]
list6 = ["bear", "orange", "butterfly", "billy"]


def task2():
    print('muchcodewow'[:4])


def task3():
    res = requests.get('http://kispython.ru/').text
    file = open("C:/PythonDel/index.html", "w")
    file.write(res)
    file.close()
    with open("C:/PythonDel/index.html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        mydivs = soup.findAll("a", {"class": "btn"})
        for div in mydivs:
            print(div.text)


def task4():
    [0xf or _ in 'abc']


def task5():
    data = [
        ['Коллеги,', 'В то же время,', 'Однако,', 'Тем не менее,', 'Следовательно,',
         'Соответственно,', 'Вместе с тем,', 'С другой стороны,'],
        ['парадигма цифровой экономики', 'контекст цифровой трансформации', 'диджитализация бизнес-процессов',
         'прагматичный подход к цифровым платформам', 'совокупность сквозных технологий',
         'программа прорывных исследований',
         'ускорение блокчейн-транзакций', 'экспоненциальный рост Big Data'],
        ['открывает новые возможности для', 'выдвигает новые требования', 'несёт в себе риски',
         'расширяет горизонты', 'заставляет искать варианты', 'не оставляет шанса для',
         'повышает вероятность', 'обостряет проблему'],
        ['дальнейшего углубления', 'бюджетного финансирования', 'синергетического эффекта',
         'компрометации конфиденциальных', 'универсальной коммодитизации', 'несанкционированной кастомизации',
         'нормативного регулирования', 'практического применения'],
        ['знаний и компетенций.', 'непроверенных гипотез.', 'волатильных активов.', 'опасных экспериментов.',
         'государственно-частных партнёрств.', 'цифровых следов граждан.', '	нежелательных последствий.',
         'внезапных открытий.']
    ]
    for i in range(2):
        for j in range(0, 5):
            print(data[j][random.randint(0, 7)], end=' ')
        print()


def myPrint(*text):
    toPrint = ""

    if len(text) > 1:
        for val in text:
            toPrint += str(val) + ' '
    else:
        toPrint = str(*text)

    toPrint += '\n'

    sys.stdout.write(toPrint)


def task6():
    myPrint("hello", 5)


def task7(*, var1, var2, var3):
    myPrint(var1, var2, var3)


def surnameGen():
    vowels = "бвгджзйклмнпрстфхцчшщ"
    consonants = "аеёиоуыэюя"
    endings = ["ов", "як", "ин", "ян", "ий", "ич"]
    result = ""
    for i in range(random.randint(1, 3)):
        result += random.choice(vowels)
        result += random.choice(consonants)
        result += random.choice(vowels)

    result += random.choice(endings)
    result = result.capitalize()

    return result


def task8():
    names = ["Авигдор", "Авксентий", "Авнер", "Аврелий", "Борислав", "Боян", "Бронислав", "Варлам", "Варнава",
             "Варсонофий",
             "Герхард", "Гессий", "Гильем", "Гинкмар", "Глеб", "Майнхард", "Макар", "Макарий", "Максим",
             "Реститут", "Ричард", "Роберт", "Родерик", "Феофил", "Феофилакт", "Фердинанд", "Ференц"]
    patronymics = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"

    res = "{name} {patr}. {surname}".format(name=random.choice(names), patr=random.choice(patronymics), surname=surnameGen())

    return res


def task9():
    a = 1
    b = 1
    c = 300000  # проверено в Python 3.10
    d = 300000
    print(a is b, c is d)  # python кэширует короткие строки и числа

    a, b = 'py', 'py'
    c = ''.join(['p', 'y'])
    print(a is b, a == c, a is c)


def parse_subj(text):
    reg = re.compile("[А-Яа-я]{1}(_)[0-9]+")
    result = reg.match(text)

    return result is not None


def task10():
    print(parse_subj("К_3"))


def encode_bwt(text):
    text += '\0'
    table = sorted(text[i:] + text[:i] for i in range(len(text)))
    last_colum = [row[-1] for row in table]
    return "".join(last_colum)


def decode_bwt(code):
    table = [""] * len(code)
    for i in range(len(code)):
        table = sorted(code[i] + table[i] for i in range(len(code)))
    s = [row for row in table if row.endswith('\0')][0]
    return s.rstrip('\0')


def rle_encode(text):
    return [(k, len(list(g))) for k, g in groupby(text)]


def task11():
    text = "hello world"
    code = encode_bwt(text)
    print(code)
    print(decode_bwt(code))
    print(rle_encode(text))


def task12():
    mdRead = open(r"C:/PythonDel/text.md", 'r')
    text = mdRead.readlines()
    mdRead.close()
    closed = True
    mdWrite = open(r"C:/PythonDel/text.md", 'w')
    for i in range(len(text)):
        for j in range(len(text[i])):
            if text[i][j] == '"':
                if closed:
                    text[i] = text[i][:j] + "<" + text[i][j + 1:]
                    closed = False
                else:
                    text[i] = text[i][:j] + ">" + text[i][j + 1:]
                    closed = True
        mdWrite.write(text[i])
    mdWrite.close()


dot = gr.Digraph(comment='Task 13')


def recurTraverse(currPath):
    for i in os.listdir(currPath):
        dot.node(currPath + '/' + i, i)
        dot.edge(currPath, currPath + '/' + i)
        if os.path.isdir(currPath + '/' + i):
            recurTraverse(currPath + '/' + i)


def task13():
    pth = "C:/PythonDel/InfoBase"
    dot.node(pth, pth)
    recurTraverse(pth)
    dot.render('Task13', view=True)


def printTable(labels, rows):
    table = PrettyTable()

    table.field_names = labels
    for row in rows:
        table.add_row(row)

    print(table)


def task14():
    rows = [
        [12, 564, 654], [432, 54, 65], [53, 342, 76], [5435, 355235, 532], [13213, 8768, 70546], [432432, 23532, 24]
    ]
    printTable(["col1", "col2", "col3"], rows)


if __name__ == '__main__':
    task1(list1, list2, list3, list4, val, list5, list6)
    task2()
    task3()
    # task4()
    task5()
    task6()
    # task7("st", "str", "str3")  #вызовет ошибку
    print(task8())
    task9()
    task10()
    task11()
    task12()
    task13()
    task14()