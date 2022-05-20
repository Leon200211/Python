from random import randint
from tkinter import Tk, Canvas, Button
import numpy as np
import requests
import graphviz


# Task_1: Р РµР°Р»РёР·Р°С†РёСЏ С…РµС‰-С„СѓРЅРєС†РёРё


class HashTable:
    def __init__(self, size):
        self.size = size
        self.Table = [[0] * 2 for i in range(size)]
        self.next = 0

    def insertData(self, newKey, newValue):
        index = hash(newKey) % self.size
        while self.Table[index][0] != 0:
            index += 1
        self.Table[index][0] = newKey
        self.Table[index][1] = newValue

    def size(self):
        return self.size()

    def delete(self, key):
        index = hash(key) % self.size()
        self.Table[index][0] = 0
        self.Table[index][1] = 0

    # РїСЂРµРІСЂР°С‰Р°РµРј С‚Р°Р±Р»РёС†Сѓ РІ РёС‚РµСЂР°С‚РѕСЂ
    def __str__(self):
        form = '{ \n'
        for obj in self.Table:
            if obj[0] != 0:
                form += "    {key}: {val}, \n".format(key=obj[0], val=obj[1])
        return form + '}'

    def __next__(self):
        while self.next < self.size:
            item = self.Table[self.next]
            if item[0] != 0:
                self.next += 1
                return item
            self.next += 1
        raise StopIteration

    def __iter__(self):
        return self


def Task_1():
    print('Task_1 :')
    lilDict = HashTable(10)
    lilDict.insertData('frog', 123)
    lilDict.insertData('bro', 13)
    print(lilDict)
    for obj in lilDict:
        print(obj)
    print('\n')


# Task_2 РСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ РІСЃС‚СЂРѕРµРЅРЅС‹С… С„СѓРЅРєС†РёР№

def GetParams(obj):
    return obj.__dict__.keys()


def Test():
    print('2 + 2 = 5000')


def TrigMethod(mtd_name):
    return globals()[mtd_name]()


def Task_2():
    print('Task_2 :')
    testTable = HashTable(6)
    print(GetParams(testTable))
    TrigMethod('Test')
    print('\n')


# Task_3 - РѕРїРёСЃР°РЅРёРµ РѕС€РёР±РєРё

def Task_3():
    print('Task_3 :')
    print('РїСЂРѕР±Р»РµРјР° РІ РЅРµРєРєРѕСЂРµРєС‚РЅРѕРј РЅР°СЃР»РµРґРѕРІР°РЅРёРё')
    print('\n')


# Task_4

class Num:
    def __init__(self, val):
        self.value = val


class Mul:
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2


class Add:
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2


class PrintVisitor(object):
    def visit(self, data):
        methods = {
            Add: self.visitAdd,
            Mul: self.visitMul,
            Num: self.visitNum
        }

        method = methods.get(type(data))
        return method(data)

    def visitAdd(self, objects):
        return f'({self.visit(objects.obj1)} + {self.visit(objects.obj2)})'

    def visitMul(self, objects):
        return f'({self.visit(objects.obj1)} * {self.visit(objects.obj2)})'

    def visitNum(self, objects):
        return f'{objects.value}'


class StackVisitor(object):
    def __init__(self):
        self.code = ''

    def get_code(self):
        return self.code

    def visit(self, data):
        methods = {
            Add: self.visitAdd,
            Mul: self.visitMul,
            Num: self.visitNum
        }

        method = methods.get(type(data))
        method(data)

    def visitAdd(self, objects):
        self.visit(objects.obj1)
        self.visit(objects.obj2)
        self.code += 'ADD \n'

    def visitMul(self, objects):
        self.visit(objects.obj1)
        self.visit(objects.obj2)
        self.code += 'MUL \n'

    def visitNum(self, objects):
        self.code += f'PUSH {objects.value} \n'


class CalcVisitor(object):
    def visit(self, data):
        methods = {
            Add: self.visitAdd,
            Mul: self.visitMul,
            Num: self.visitNum
        }

        method = methods.get(type(data))
        return method(data)

    def visitAdd(self, objects):
        return self.visit(objects.obj1) + self.visit(objects.obj2)

    def visitMul(self, objects):
        return self.visit(objects.obj1) * self.visit(objects.obj2)

    def visitNum(self, objects):
        return objects.value


def Task_4():
    print('Task_4 :')
    ast = Add(Num(7), Mul(Num(3), Num(2)))
    pv = PrintVisitor()
    cv = CalcVisitor()
    sv = StackVisitor()
    print(pv.visit(ast))
    print(cv.visit(ast))
    sv.visit(ast)
    print(sv.get_code())
    print('\n')


# Task_5

class HTML:
    def __init__(self):
        self.code = []
        self.last = 0

    def body(self):
        self.code.insert(self.last, '<body>')
        self.code.append('</body>')
        self.last += 1
        return self

    def div(self):
        self.code.insert(self.last, '<div>')
        self.code.insert(self.last + 1, '</div>')
        self.last += 2
        return self

    def p(self, text):
        self.code.insert(self.last, f'<p>{text}</p>')
        self.last += 1
        return self

    def get_code(self):
        result = ''
        for obj in self.code:
            result += obj + '\n'
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


def Task_5():
    html = HTML()
    with html.body():
        with html.div():
            with html.div():
                html.p('РџРµСЂРІР°СЏ СЃС‚СЂРѕРєР°.')
                html.p('Р’С‚РѕСЂР°СЏ СЃС‚СЂРѕРєР°.')
            with html.div():
                html.p('РўСЂРµС‚СЊСЏ СЃС‚СЂРѕРєР°.')
    print(html.get_code())


# Task_6

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

NODE_R = 15

C1 = 2
C2 = 100
C3 = 10000
C4 = 0.1

DELAY = 10


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, text):
        self.text = text
        self.targets = []
        self.vec = Vec(0, 0)

    def to(self, *nodes):
        for n in nodes:
            self.targets.append(n)
            n.targets.append(self)
        return self


class Graph:
    def __init__(self):
        self.nodes = []

    def add(self, text):
        self.nodes.append(Node(text))
        return self.nodes[-1]


class GUI:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=CANVAS_WIDTH,
                             height=CANVAS_HEIGHT, bg="white")
        self.draw_button = Button(root, text="Draw", command=self.start_draw)
        self.canvas.pack()
        self.draw_button.pack()
        self.nodes = None
        self.busy = None

    def draw_node(self, x, y, text, r=NODE_R):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="MistyRose2")
        self.canvas.create_text(x, y, text=text)

    def draw_graph(self):
        for n in self.nodes:
            for t in n.targets:
                self.canvas.create_line(n.vec.x, n.vec.y, t.vec.x, t.vec.y)
        for n in self.nodes:
            self.draw_node(n.vec.x, n.vec.y, n.text)

    def start_draw(self):
        self.canvas.delete("all")
        if self.busy:
            self.root.after_cancel(self.busy)

        random_layout(self.nodes)
        force_layout(self.nodes)

        self.animate()

    def animate(self):
        self.canvas.delete("all")
        for _ in range(DELAY):
            force_layout(self.nodes)
        self.draw_graph()
        self.busy = self.root.after(5, self.animate)


def random_layout(nodes):
    for n in nodes:
        n.vec.x = randint(NODE_R * 4, CANVAS_WIDTH - NODE_R * 4 - 1)
        n.vec.y = randint(NODE_R * 4, CANVAS_HEIGHT - NODE_R * 4 - 1)


def f_spring(u, v):
    a = u.vec.x - v.vec.x
    b = u.vec.y - v.vec.y
    unit = np.array([a, b])
    unitMod = np.sqrt(np.power(a, 2) + np.power(b, 2))
    return np.divide(unit, unitMod) * C1 * np.log(np.divide(unitMod, C2))


def f_ball(u, v):
    a = u.vec.x - v.vec.x
    b = u.vec.y - v.vec.y
    unit = np.array([a, b])
    unitMod = np.sqrt(np.power(a, 2) + np.power(b, 2))
    return np.divide(unit, unitMod) * C1 * np.log(np.divide(C3, np.power(unitMod, 2)))


def force_layout(nodes):
    for u in nodes:
        forces = [0, 0]
        for v in nodes:
            if u is not v:
                w1, w2 = f_spring(u, v), f_ball(u, v)
                forces[0] = forces[0] + w1[0] + w2[0]
                forces[1] = forces[1] + w1[1] + w2[1]

        u.vec.x += forces[0]
        u.vec.y += forces[1]


def Task_6():
    g = Graph()
    n1 = g.add("1")
    n2 = g.add("2")
    n3 = g.add("3")
    n4 = g.add("4")
    n5 = g.add("5")
    n6 = g.add("6")
    n7 = g.add("7")
    n1.to(n2, n3, n4, n5)
    n2.to(n5)
    n3.to(n2, n4)
    n6.to(n4, n1, n7)
    n7.to(n5, n1)

    root = Tk()
    w = GUI(root)
    w.nodes = g.nodes
    root.mainloop()


# Task_7 - РёРµСЂР°СЂС…РёС‡РµСЃРєР°СЏ РєР»Р°СЃС‚РµСЂРёР·Р°С†РёСЏ

def load_csv(filename):
    text = requests.get(filename).text
    rows = []
    for line in text.split('\n')[1:]:
        rows.append(line.split(';'))
    return rows[:len(rows) - 1]


class Cluster:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


def jaccard_dist(row1, row2):
    A, B, C = 0, 0, 0
    for i in range(1, len(row1)):
        if row1[i] == "1" and row2[i] == "1":
            A += 1
            B += 1
            C += 1
        elif row1[i] == "1":
            A += 1
        elif row2[i] == "1":
            B += 1
    if A + B - C == 0:
        return 1
    return C / (A + B - C)


def cluster_dist(func, data1, data2):
    return func(data1.data, data2.data)


def hclust(rows):
    clusters = [Cluster(row) for row in rows]  # Р§СѓС‚РѕРє РјРѕРґРёС„РёС†РёСЂРѕРІР°Р»
    counter = 0
    while len(clusters) > 1:
        for i in clusters:
            d = 0
            target = clusters[(clusters.index(i) + 1) % len(clusters)]
            for j in clusters:
                if i != j:
                    if cluster_dist(jaccard_dist, i, j) > d:
                        d = cluster_dist(jaccard_dist, i, j)
                        target = j
            a = ["c" + str(counter)]
            for k in range(1, len(i.data)):
                if i.data[k] == "1" or target.data[k] == "1":
                    a.append("1")
                else:
                    a.append("0")
            clusters.append(Cluster(a, i, target))
            clusters.remove(i)
            clusters.remove(target)
            counter += 1
    return clusters[0]


def gen_dot(cluster):
    dot = graphviz.Digraph()
    clusters = [cluster]
    dot.node(clusters[0].data[0])
    while len(clusters) > 0:
        if clusters[0].left is not None:
            dot.node(clusters[0].left.data[0])
            clusters.append(clusters[0].left)
            dot.edge(clusters[0].data[0], clusters[0].left.data[0])
        if clusters[0].right is not None:
            dot.node(clusters[0].right.data[0])
            clusters.append(clusters[0].right)
            dot.edge(clusters[0].data[0], clusters[0].right.data[0])
        clusters.remove(clusters[0])
    return dot


def Task_7():
    print('Task_7 : ')
    rows = load_csv("https://raw.githubusercontent.com/true-grue/kispython/main/data/langs.csv")
    cluster = hclust(rows)
    print(gen_dot(cluster))
    # gen_dot(cluster).render('test-output/test-table.gv', view=True)


if __name__ == '__main__':
    Task_1()
    Task_2()
    Task_3()
    Task_4()
    Task_5()
    Task_6()
    Task_7()