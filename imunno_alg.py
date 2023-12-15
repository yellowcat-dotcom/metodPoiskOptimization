import random


# Функция Розенброка
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


# сжатие популяции
def compress(population, value):
    flag = True
    while flag:
        flag = False
        new_population = population.copy()
        # Для каждой пары антител
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                if population[i] != [] and population[j] != []:
                    # Если расстояние меньше заданного значения
                    if affin(population[i], population[j]) < value:
                        flag = True
                        # Оставляем только антитело с более низким значением функции Розенброка
                        if rosenbrock(population[i][0], population[i][1]) < rosenbrock(population[j][0], population[j][1]):
                            population[j] = []
                        else:
                            population[i] = []
    # Удаляем "пустые" антитела
    population = list(filter(lambda a: a != [], population))
    return population


# клонирование и мутация некоторых антител
def clone_and_mutate(antibodies, nc, alpha, nd, gen, bb, br):
    clones = []
    for body in antibodies:
        clones = []
        # Создание клонов с мутациями
        for c in range(nc):
            clones.append([body[0] + alpha * random.uniform(-0.5, 0.5), body[1] + alpha * random.uniform(-0.5, 0.5)])
    clones.sort(key=lambda a: affin(a, gen), reverse=False)
    Sm = clones[:nd]

    # Удаляем из популяции S^m те клетки, аффинность которых ниже величины b_b
    for i in range(nd):
        if affin(Sm[i], gen) < bb:
            Sm = Sm[:i]
            break
    # клональное сжатие
    Sm = compress(Sm, br)
    return Sm


# получаем лучшие антитела
def get_best_antibodies(antibodies, antigen, nb):
    sub_antibodies = antibodies.copy()
    # Сортировка по близости к антигену
    sub_antibodies.sort(key=lambda x: affin(x, antigen), reverse=False)
    sub_antibodies = sub_antibodies[:nb]
    return sub_antibodies


# создание популяции клеток памяти
def create_Sm(Sb, Sg, nb, nc, alpha, nd, bb, br):
    for gen in Sg:
        # 2.1 выбираем лучшие антитела по близости к гену
        antibodies = get_best_antibodies(Sb, gen, nb)
        # 2.2 выполяем клонирование и мутацию
        Sm = clone_and_mutate(antibodies, nc, alpha, nd, gen, bb, br)
        # Объединяем популяцию и выполняем сжатие
        Sb += Sm
        Sb = compress(Sb, br)
    return Sb


'''
Параметры:
1-4. Минимальные и максимальнве значения координат     minx, maxx, miny, maxy
5. Размер начальной популяции антител                  Sb
6. Размер начальной популяции антигенов                Sg
7. Число антител для мутации                           nb
8. Число оставляемых клонов                            nd
9. Число клонов клонируемого антитела                  nc
10. Коэффициент мутации                                alpha
11. количество итераций                                iterations
12. Пороговый коэффициент гибели                       bb
13. Коэффициент клонального сжатия                     br
'''


# print(immun_algorithm(-6, 6, -6, 6, 100, 50, 10, 5, 7, 0.3, 100, 0.4, 0.4))

def immun_algorithm(minx, maxx, miny, maxy, Sb, Sg, nb, nd, nc, alpha, iterations, bb, br):
    # 1 Генерация начальных популяций антител и антигенов, получаем список с координатами
    Sb = generate_population(minx, maxx, miny, maxy, Sb)
    Sg = generate_population(minx, maxx, miny, maxy, Sg)

    for i in range(iterations):
        # Создание клеток памяти
        Sb = create_Sm(Sb, Sg, nb, nc, alpha, nd, bb, br)

    # Находим лучшее антитело и его значение функции Розенброка
    mn = rosenbrock(Sb[0][0], Sb[0][1])
    idx = 0
    for i in range(1, len(Sb)):
        if rosenbrock(Sb[i][0], Sb[i][1]) < mn:
            idx = i
            mn = rosenbrock(Sb[i][0], Sb[i][1])
    # Возвращаем результат
    return [Sb[idx], mn]


print(immun_algorithm(-6, 6, -6, 6, 100, 50, 10, 5, 7, 0.3, 100, 0.4, 0.4))
