import numpy as np
from scipy.stats import uniform
from sklearn.metrics import euclidean_distances
import sys

# Определите единообразные распределения для мутации и инициализации
UNIFORM_CHANGE = uniform(-0.5, 1)
UNIFORM_START = uniform(-2, 4)


# Функция Розенброка для оптимизации
def rosenbrock(x):
    return np.sum(100 * (x.T[1:] - x.T[:-1] ** 2.0) ** 2 + (1 - x.T[:-1]) ** 2.0, axis=0)


# Инициализируйте совокупность случайным образом в пределах заданного диапазона
def init_population(population_size, problem_size):
    pop = UNIFORM_START.rvs(population_size * problem_size)
    pop = pop.reshape((population_size, problem_size))
    return pop


def eval_population(f, population):
    return np.array([f(x) for x in population])


# Создавать клоны
def create_clones(cell, n):
    return np.array([cell] * n)


# Измените индивидуума, добавив случайное значение из равномерного распределения
def mutate(clone, alpha):
    return clone + UNIFORM_CHANGE.rvs(len(clone)) * alpha


def affinity_suppress(f, population, affinity_thresh):
    new_population = []
    for cell in population:
        # Найдите соседей на определенном расстоянии
        neighbors = np.array([neighbor for neighbor in population if 0 < euclidean_distances(neighbor.reshape(1, -1), cell.reshape(1, -1)) < affinity_thresh])

        neig_eval = eval_population(f, neighbors)

        if not len(neighbors):
            new_population.append(cell)
            continue
        best_neighbor = neighbors[np.argmin(neig_eval)]
        new_population.append(cell if f(cell) < f(best_neighbor) else best_neighbor)
    return new_population

# Внедрить алгоритм оптимизации искусственной иммунной системы
def immune_system(problem_size, population_size=40, nclones=3, iters=70, affinity_thresh=0.1, mutation_rate=0.3):
    # Инициализировать совокупность антител
    population = init_population(population_size, problem_size)
    #print(len(population))
    min_cost = []

    # Основной цикл оптимизации
    for _ in range(iters):
        # клонирование и мутация
        for i, cell in enumerate(population):
            #print(cell)
            clones = create_clones(cell, nclones)
            clones = [mutate(clone, mutation_rate) for clone in clones]
            #print(clones)
            # Оценка пригодности клонов
            clones_eval = eval_population(rosenbrock, clones)
            #print(clones_eval)

            # Выбираем одного лучшего клона
            population[i] = clones[np.argmin(clones_eval)]
            #print(population[i])

        # Применить сжатие
        #время от размерности, целевая функция о итерациях
        #print(len(population))
        population = affinity_suppress(rosenbrock, population, affinity_thresh)
        #print(len(population))

        # Оценка пригодности популяции
        pop_eval = eval_population(rosenbrock, population)


        best_cost, best_individual = np.min(pop_eval), population[np.argmin(pop_eval)]
        #print(best_cost, best_individual)
        min_cost.append((best_cost, best_individual))


    # Возвращает наилучший результат, основанный на минимальной стоимости
    return min(min_cost, key=lambda x: x[0])



best_result = immune_system(2, 40, 3, 70, 0.1, 0.3)
#print(best_result[1][0], best_result[1][1], best_result[0])
