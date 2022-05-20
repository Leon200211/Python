import numpy as np


table = np.array([ [1, 3, 3, 8, 20],
                   [8, 6, 2, 6, 20],
                   [5, 2, 4, 5, 45],
                   [25, 5, 40, 15, 85],
                   ])
table = np.pad(np.expand_dims(table, axis=2), ((0,0), (0,0), (0,1))) #создаем вторую подтаблицу с планом
for i in table[:-1] : i[-1][1] = i[-1][0]
# выводи две подтаблицы
print("Исходная таблица")
print(table[:, :, 0])
print(table[:, :, 1])


#~================================================
# создаем первый план
def stage_1(table):
    j = 0
    i = 0
    while j < len(table[0]) - 1 and i < len(table) - 1:
        need = table[:, j][-1][0] - table[:, j][-1][1] #потребности - остаток
        resourse = table[i, -1][1]
        if need >= resourse:
            # если исчерпали запас
            table[i, j, 1] = resourse
            table[:, j][-1][1] += resourse
            table[i, -1, 1] = 0
            i += 1
        else:
            table[i, j, 1] = need
            table[i, -1, 1] -= need
            table[:, j][-1][1] += need
            j += 1

stage_1(table)
print("========================================")
print("Этап I. Нахождение первого опорного плана")
# выводи две подтаблицы
print(table[:, :, 0])
print(table[:, :, 1])
print("Общая стоимость перевозок составляет f =", end=" ")
print(sum(sum(table[:-1, :-1, 0] * table[:-1, :-1, 1])))




#~================================================
# функция для подсчета ∆
def estimate(table):

    # Далее для каждой заполненной клетки находим относительные оценки
    B = np.concatenate(table[:-1, :-1, 0])
    M = np.zeros(((len(table) - 1) * (len(table[0]) - 1), (len(table) - 1) + (len(table[0]) - 1) ))
    for i in range(len(table) - 1):
        for j in range(len(table[0]) - 1):
            if table[i, j, 1] != 0:
                M[i * (len(table[0]) - 1) + j, i] = 1
                M[i * (len(table[0]) - 1) + j, len(table) - 1 + j] = 1

    M = np.concatenate((M, np.expand_dims(B, 1)), axis=1)
    to_del = []
    for i in range(len(M)):
        if(np.count_nonzero(M[i][:-1]) == 0):
            to_del.append(i)


    # высчитываем дельты по формуле ∆𝑖𝑗= 𝑐𝑖𝑗 − (𝑢𝑖 + 𝑣𝑗)
    M = np.delete(M, to_del, 0)
    UV = np.linalg.solve(M[:, 1:-1], M.T[-1])
    U = np.concatenate((np.array([0]), UV[:len(table) - 2]), axis=0)
    V = UV[len(table) - 2:]

    deltas = []

    for i in range(len(table) - 1):
        for j in range(len(table[0]) - 1):
            if table[i, j, 1] == 0:
                # добавляем в массив дельты с координатоми ячеек
                deltas.append((i, j, table[i, j, 0] - (U[i] + V[j])))
    return deltas



#~================================================
# функция по поиску след ячейки цикла
def get_next(map, start):
    # map - Таблица с вычисленными потенциалами
    # со значением -1 в ячейке где начинается цикл
    # start - координаты ячейки где начинается цикл
    next = []
    i, j = start[0], start[1]
    # i, j - х. у. по таблице
    # далее в next заполняются координаты двух направлений цикла
    while i < len(map):
        if i != start[0]:
            if(map[i][start[1]] != 0):
                next.append((i, start[1]))
                break
        i+=1
    i = start[0]
    while i > -1:
        if i != start[0]:
            if(map[i][start[1]] != 0):
                next.append((i, start[1]))
                break
        i-=1
    while j < len(map[0]):
        if j != start[1]:
            if(map[start[0]][j] != 0):
                next.append((start[0], j))
                break
        j+=1
    j = start[1]
    while j > -1:
        if j != start[1]:
            if(map[start[0]][j] != 0):
                next.append((start[0], j))
                break
        j-=1
    return next


#~================================================
# создаем новый цикл для решения
def get_new_circle(point, map, visited):
    # point - номера ячеек куда переходит цикл
    # map - Таблица для вычисления потенциала
    # visited - координаты ходов для текущего цикла ( не полного )
    v = [point]
    paths = []
    # get_next - функция по поиску след ячейки цикла
    for next in get_next(map, point):
        #next - координаты след ячейки цикла
        if next == visited[0] and len(visited) > 2:
            paths.append([next])
        elif next not in visited:
            # рекурсивно вызывается функция для поиска новых координат
            res = get_new_circle(next, map, visited + [next])
            if len(res) > 0 : paths.append(res)
    # paths - все варианты пути и направления цикла
    if len(paths) > 0:
        v += min(paths, key=lambda i: len(i))
        # v - координаты ходов для полного цикла цикла
        return v
    else: return []


#~================================================
# эта функция нужна чтобы убрать повторяющиеся координаты из цикла
def solve_circle(circle):
    i = 1
    # circle - координаты ячеек полного наилучшего цикла
    while i < len(circle) - 1:
        if circle[i-1][0] == circle[i][0] == circle[i+1][0]:
            circle.remove(circle[i])
        else:
            i += 1
    j = 1
    while j < len(circle) - 1:
        if circle[j-1][1] == circle[j][1] == circle[j+1][1]:
            circle.remove(circle[j])
        else:
            j += 1
    # координаты цикла без повторяющихся ячеек
    return circle


#~================================================
# основной цикл пока есть отрицательные ∆
def iterate(table):
    iter = 0
    # считаем ∆
    deltas = estimate(table)
    # пока относительные оценки отрицательны
    while min(deltas, key=lambda i: i[2])[2] < 0:
        iter += 1

        # выводим информациб в консоль
        print("\nИтерация №", iter)
        print("Дельты")
        for i in range(len(deltas)):
            print(deltas[i][2], end=" ")
        print("\nДо изменения")
        print(table[:, :, 0])
        print(table[:, :, 1])




        # находим наименьшую отрицательную оценку
        new = min(deltas, key=lambda i: i[2])
        # создаем копию для работы цикла
        map = table[:-1, :-1, 1].copy()
        map[new[0], new[1]] = -1
        # задаем стартовую точку для начада цикла
        start = (new[0], new[1])
        # создаем цикл
        circle = get_new_circle(start, map, [start])
        # решаем проблему повторяющихся ячеек
        circle = solve_circle(circle)
        #Найдем 𝜆 = min равное наименьшему из чисел, стоящих в отрицательных вершинах цикла
        l = map[min(circle[1:-2], key=lambda i: map[i])]
        #Двигаясь далее по означенному циклу, +- 𝜆
        for i in range(0, len(circle) - 1, 2):
            table[circle[i]][1] += l
            table[circle[i + 1]][1] -= l
        deltas = estimate(table)

        print("После изменения")
        print(table[:, :, 0])
        print(table[:, :, 1])
        print("Общая стоимость перевозок составляет f =", end=" ")
        print(sum(sum(table[:-1, :-1, 0] * table[:-1, :-1, 1])))



print("============================================")
print("Этап II. Улучшение опорного плана")
iterate(table)
table[:, :, 1]

print("\n============================================")
print("Plan: ")
print(table[:-1, :-1, 1])
print("Result: ")
print(sum(sum(table[:-1, :-1, 0] * table[:-1, :-1, 1])))