# /use/bin/env python3
# coding: UTF-8

import random


# Функция Розенброка (целевая)
def rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2



# расстояние между точками
def affin(x, y):
    return (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2


# генерация начальной популяции
def generate_population(minx, maxx, miny, maxy, num):
    population = []
    for i in range(num):
        population.append([random.uniform(minx, maxx), random.uniform(miny, maxy)])
    return population


# сжатие популяции (неважно какой)
# value - наименьшая аффинность
def compress(population, value):
    flag = True
    while flag:
        flag = False
        new_population = population.copy()
        # для каждого элемента
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                if population[i] != [] and population[j] != []:
                    if affin(population[i], population[j]) < value:
                        flag = True
                        if rosenbrock(population[i][0], population[i][1]) < rosenbrock(population[j][0],
                                                                                       population[j][1]):
                            population[j] = []
                        else:
                            population[i] = []
    population = list(filter(lambda a: a != [], population))
    return population


# клонирование и мутация некоторых антител
def clone_and_mutate(antibodies, nc, alpha, nd, gen, bb, br):
    clones = []
    for body in antibodies:
        clones = []
        for c in range(nc):
            clones.append([body[0] + alpha * random.uniform(-0.5, 0.5), body[1] + alpha * random.uniform(-0.5, 0.5)])
    clones.sort(key=lambda a: affin(a, gen), reverse=False)
    Sm = clones[:nd]
    for i in range(nd):
        if affin(Sm[i], gen) < bb:
            Sm = Sm[:i]
            break
    Sm = compress(Sm, br)
    return Sm


# получаем лучшие антитела
def get_best_antibodies(antibodies, antigen, nb):
    sub_antibodies = antibodies.copy()
    sub_antibodies.sort(key=lambda x: affin(x, antigen), reverse=False)
    sub_antibodies = sub_antibodies[:nb]
    return sub_antibodies


# создание популяции клеток памяти
def create_Sm(Sb, Sg, nb, nc, alpha, nd, bb, br):
    for gen in Sg:
        antibodies = get_best_antibodies(Sb, gen, nb)
        Sm = clone_and_mutate(antibodies, nc, alpha, nd, gen, bb, br)
        Sb += Sm
        Sb = compress(Sb, br)
    return Sb


'''
Параметры:
1-4. Минимальные и максимальнве значения координат
5. Размер начальной популяции антител
6. Размер начальной популяции антигенов
7. Число антител для мутации
8. Число оставляемых клонов
9. Число клонов клонируемого антитела
10. Коэффициент мутации
11. количество итераций
12. Пороговый коэффициент гибели
13. Коэффициент клонального сжатия
'''


def immun_algorithm(minx, maxx, miny, maxy, Sb, Sg, nb, nd, nc, alpha, iterations, bb, br):
    Sb = generate_population(minx, maxx, miny, maxy, Sb)
    Sg = generate_population(minx, maxx, miny, maxy, Sg)
    for i in range(iterations):
        Sb = create_Sm(Sb, Sg, nb, nc, alpha, nd, bb, br)

    mn = rosenbrock(Sb[0][0], Sb[0][1])
    idx = 0
    for i in range(1, len(Sb)):
        if rosenbrock(Sb[i][0], Sb[i][1]) < mn:
            idx = i
            mn = rosenbrock(Sb[i][0], Sb[i][1])
    # print(Sb[idx],mn)
    return [Sb[idx], mn]

print(immun_algorithm(-6,6,-6,6,100,50,10,5, 7,0.3,100,0.4,0.4))