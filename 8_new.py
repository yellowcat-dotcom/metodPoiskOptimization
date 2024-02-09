
import numpy as np
from scipy.stats import uniform
from sklearn.metrics import euclidean_distances
import time

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
        neighbors = np.array([neighbor for neighbor in population if
                              0 < euclidean_distances(neighbor.reshape(1, -1), cell.reshape(1, -1)) < affinity_thresh])

        neig_eval = eval_population(f, neighbors)

        if not len(neighbors):
            new_population.append(cell)
            continue
        best_neighbor = neighbors[np.argmin(neig_eval)]
        new_population.append(cell if f(cell) < f(best_neighbor) else best_neighbor)
    return new_population



def gradient_descent(initial_point, epsilon1, epsilon2, max_iters):
    current_point = initial_point.copy()
    k = 0

    for k in range(max_iters):

        f_current = rosenbrock(current_point)

        # Шаг 4: Проверить выполнение критерия окончания

        if np.abs(f_current) < epsilon1:
            print("точность")
            print("np.abs(f_current) < epsilon1:", np.abs(f_current), epsilon1)
            return current_point, k

        # Шаг 5: Проверить выполнение неравенства
        if k >= max_iters:
            print("число итераций")
            return current_point, k

        # Шаг 6: Задать величину шага tk
        tk = 1e-5  # Пример значения, может потребоваться настройка

        # Шаг 7: Вычислить xk+1
        next_point = current_point - tk * np.gradient(current_point)

        # Шаг 8: Проверить выполнение условия
        if rosenbrock(next_point) - f_current < 0:
            print("if rosenbrock(next_point) - f_current < 0:")
            current_point = next_point
        else:
            tk /= 2  # Уменьшить шаг
            print("новый шаг", tk)

        # Шаг 9: Проверить выполнение условий
        if np.linalg.norm(next_point - current_point) < epsilon2 and np.abs(rosenbrock(next_point) - f_current) < epsilon2:
            print("Последнее условие с нормой")
            return next_point, k + 1
    print("k=",k)

    return current_point, k

# Внедрить гибридный метод оптимизации
def hybrid_optimization(problem_size, population_size=40, nclones=3, iters=70, affinity_thresh=0.1, mutation_rate=0.3):

    start_time = time.time()
    # Инициализировать совокупность антител
    population = init_population(population_size, problem_size)
    min_cost = []

    # Основной цикл оптимизации
    for _ in range(iters):
        # клонирование и мутация
        for i, cell in enumerate(population):
            clones = create_clones(cell, nclones)
            clones = [mutate(clone, mutation_rate) for clone in clones]
            clones_eval = eval_population(rosenbrock, clones)

            # Выбираем одного лучшего клона
            population[i] = clones[np.argmin(clones_eval)]

        # Применить сжатие
        population = affinity_suppress(rosenbrock, population, affinity_thresh)

        # Оценка пригодности популяции
        pop_eval = eval_population(rosenbrock, population)

        best_cost, best_individual = np.min(pop_eval), population[np.argmin(pop_eval)]
        min_cost.append((best_cost, best_individual))

    # Применить метод градиентного спуска как постпроцессор
    best_solution = min(min_cost, key=lambda x: x[0])[1]
    imunn_time = time.time()
    print(best_solution, rosenbrock(best_solution))
    gradient_descent_result = gradient_descent(best_solution, 1e-10, 1e-10, 10)

    end_time = time.time()
    work_time_all = end_time - start_time

    work_time_imunn = imunn_time - start_time


    return gradient_descent_result, work_time_all, work_time_imunn



best_result, work_time, work_time_imunn = hybrid_optimization(2, 40, 3, 280, 0.1, 0.3)
best_point = best_result[0]  # Extract the point from the tuple

print("Best Result after Hybrid Optimization:", best_point, "Cost:", rosenbrock(best_point), "Time_all ", work_time, "Time_imunn ", work_time_imunn)
