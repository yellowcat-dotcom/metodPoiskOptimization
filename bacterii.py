import random;
import math


# хемотаксис, репродукция, ликвидация и рассеивание.

# сфера

def sphere(x, y):
    return -(x ** 2 + y ** 2)

# модуль вектора
def mod(x):
    return math.sqrt(x[0] ** 2 + x[1] ** 2)


# генерация бактерий с случайными координатами и скоростями
def generate(num, minx, maxx, miny, maxy):
    population = []
    for i in range(num):
        b = [[random.uniform(minx, maxx), random.uniform(miny, maxy)]]
        b.append([random.uniform(-1, 1), random.uniform(-1, 1)])
        b.append(sphere(b[0][0], b[0][1]))
        population.append(b.copy())
    return population


# Функция, представляющая хемотаксисное движение бактерии
def chemotaxis(bacteria, lmbd):
    operation = random.randint(0, 1)
    if operation == 0:
        # то движемся
        bacteria[0][0] = bacteria[0][0] + lmbd * bacteria[1][0] / (mod(bacteria[1]))
        bacteria[0][1] = bacteria[0][1] + lmbd * bacteria[1][1] / (mod(bacteria[1]))
    else:
        v = [random.uniform(-1, 1), random.uniform(-1, 1)]
        bacteria[0][0] = bacteria[0][0] + lmbd * v[0] / mod(v)
        bacteria[0][1] = bacteria[0][1] + lmbd * v[1] / mod(v)
        bacteria[1] = v
    new_value = sphere(bacteria[0][0], bacteria[0][1])
    if new_value > bacteria[2]:  # Условие для кувырка
        bacteria[2] = new_value
    else:
        bacteria[2] += new_value
    return bacteria


# Функция для репликации, выбирая лучшие особи

def reproduction(bacteries):
    count = len(bacteries)
    bacteries.sort(key=lambda a: a[2], reverse=True)
    bacteries = bacteries[:int(count / 2)]
    bacteries += bacteries.copy()
    return bacteries


# ликвидация
def elimination(bacteries, n, minx, maxx, miny, maxy):
    for i in range(n):
        x = random.randint(0, (len(bacteries) - 1))
        del bacteries[x]
        new_bacteria = generate(1, minx, maxx, miny, maxy)
        bacteries += (new_bacteria.copy())
    return bacteries


# Функция для ликвидации определенного числа бактерий и создания новых
def get_best_solution(bacteries):
    best_solution = [bacteries[0][0].copy()]
    best_solution.append(sphere(best_solution[0][0], best_solution[0][1]))
    for bac in bacteries:
        # print(bac)
        if sphere(bac[0][0], bac[0][1]) > best_solution[1]:
            best_solution[0] = bac[0].copy()
            best_solution[1] = sphere(bac[0][0], bac[0][1])
    return best_solution


'''
Параметры:
1-4 Минимальные и максимальные значения координат
5 - раззмер популяции
6 - количество итераций изменения популяции (суммарное число шагов)
7 - размер шага (скорость)
8 - количесво особей, уничтожаемых в ходе ликвидации
9 - вероятность ликвидации 
'''


def bacteria_algorithm(minx, maxx, miny, maxy, num, iterations, lmbd, n, ep):
    # Генерация начальной популяции бактерий
    population = generate(num, minx, maxx, miny, maxy)

    # Инициализация текущего лучшего решения
    current_best = get_best_solution(population)
    # Инициализация глобального лучшего решения
    global_best = current_best.copy()
    # Копия текущего лучшего решения для сравнения с будущими результатами
    bst = current_best.copy()

    for it in range(iterations):
        # Если найдено лучшее решение, чем текущее, выполняется хемотаксис
        if bst[1] <= current_best[1]:
            # Обновление текущего лучшего решения
            current_best = bst.copy()
            # Применение хемотаксиса ко всей популяции
            for i in range(len(population)):
                population[i] = chemotaxis(population[i], lmbd)

            # Поиск лучшего решения в обновленной популяции
            bst = get_best_solution(population)

        # Если текущее решение лучше, чем найденное, выполняется репликация или ликвидация
        else:
            # Генерация случайного числа для принятия решения о репликации или ликвидации
            i = random.uniform(0, 1)
            # Если случайное число больше заданной вероятности, выполняется репликация
            if i > ep:
                population = reproduction(population)
            else:  # Иначе выполняется ликвидация
                population = elimination(population, n, minx, maxx, miny, maxy)

            # Поиск лучшего решения после репликации или ликвидации
            bst = get_best_solution(population)
            # Обновление текущего лучшего решения
            current_best = bst.copy()

        # Обновление глобального лучшего решения, если необходимо
        if global_best[1] < current_best[1]:
            global_best = current_best.copy()

    # Инвертирование значения функции "сфера", так как алгоритм максимизирует, а не минимизирует
    global_best[1] = -global_best[1]

    return global_best


print(bacteria_algorithm(-3, 3, -3, 3, 10, 250, 0.1, 5, 0.1))



