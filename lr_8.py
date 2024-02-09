# Импорт библиотек
import random
from scipy import optimize
import quickest_descent

# Определение целевой функции Розенброка
def rosenbrock_function(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

# Класс для гибридного алгоритма
class HybridAlgorithm:
    array_steps = []

    def __init__(self):
        pass

    # Генерация начальной популяции
    @staticmethod
    def generate_population(num_persons, min_x, max_x, min_y, max_y):
        population = []
        for i in range(num_persons):
            population.append([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        return population

    # Метод отбора по усечению
    @staticmethod
    def get_selection_by_truncation(num_persons, population):
        new_population = []
        for i in population:
            new_population.append([rosenbrock_function(i[0], i[1]), i[0], i[1]])
        new_population.sort()

        result = []
        for i in range(num_persons):
            percent = random.uniform(0, 1)
            person = random.randint(0, int(len(new_population) * percent))
            result.append([new_population[person][1], new_population[person][2]])
        return result

    # Метод элитного отбора
    def get_elite_selection(self, num_persons, population):
        new_population = []
        for i in population:
            new_population.append([rosenbrock_function(i[0], i[1]), i[0], i[1]])
        new_population.sort()

        elite = int(num_persons * 0.1)
        result = []
        for i in range(elite):
            result.append([new_population[elite][1], new_population[elite][2]])

        n_pop = self.get_selection_by_truncation(num_persons - elite, population[elite:])
        result += n_pop
        return result

    # Метод панмиксии
    @staticmethod
    def get_panmixia(population):
        parents_pairs = []
        num_persons = len(population)
        for i in range(num_persons):
            second_parent = random.randint(0, num_persons - 1)
            parents_pairs.append([population[i], population[second_parent]])
        return parents_pairs

    # Расстояние между особями (генотип)
    @staticmethod
    def get_distance(parent1, parent2):
        return (parent1[0] - parent2[0]) ** 2 + (parent1[1] - parent2[1])

    # Метод инбридинга по генотипу
    def get_inbreeding_by_genotype(self, population):
        parents_pairs = []
        for i in range(len(population)):
            mn = self.get_distance(population[i], population[1 if i == 0 else 0])
            second_parent = 1 if i == 0 else 0

            for j in range(len(population)):
                if j != i and self.get_distance(population[i], population[j]) < mn:
                    mn = self.get_distance(population[i], population[j])
                    second_parent = j

            parents_pairs.append([population[i], population[second_parent]])

        return parents_pairs

    # Метод инбридинга по фенотипу
    @staticmethod
    def get_inbreeding_by_phenotype(population):
        parents_pairs = []
        function_values = []

        for i in range(len(population)):
            function_values.append(rosenbrock_function(population[i][0], population[i][1]))

        for i in range(len(population)):
            mn = abs(function_values[i] - function_values[1 if i == 0 else 0])
            second_parent = 1 if i == 0 else 0

            for j in range(len(population)):
                if j != i and abs(function_values[i] - function_values[j]) < mn:
                    second_parent = j
                    mn = abs(function_values[i] - function_values[j])

            parents_pairs.append([population[i], population[second_parent]])

        return parents_pairs

    # Метод аутбридинга по генотипу
    def get_outbriding_by_genotype(self, population):
        parents_pairs = []
        for i in range(len(population)):
            mx = self.get_distance(population[i], population[0])
            second_parent = 0

            for j in range(len(population)):
                if j != i and self.get_distance(population[i], population[j]) > mx:
                    mn = self.get_distance(population[i], population[j])
                    second_parent = j

            parents_pairs.append([population[i], population[second_parent]])

        return parents_pairs

    # Метод аутбридинга по фенотипу
    @staticmethod
    def get_outbriding_by_phenotype(population):
        parents_pairs = []
        function_values = []

        for i in range(len(population)):
            function_values.append(rosenbrock_function(population[i][0], population[i][1]))

        for i in range(len(population)):
            mx = abs(function_values[i] - function_values[0])
            second_parent = 0

            for j in range(len(population)):
                if j != i and abs(function_values[i] - function_values[j]) > mx:
                    second_parent = j
                    mx = abs(function_values[i] - function_values[j])

            parents_pairs.append([population[i], population[second_parent]])

        return parents_pairs

    # Метод интермедиарной рекомбинации
    @staticmethod
    def get_intermediate_recombination(parent_pairs):
        new_population = []
        for i in range(len(parent_pairs)):
            alpha_1 = random.uniform(-0.25, 1.25)
            alpha_2 = random.uniform(-0.25, 1.25)

            parent_1 = parent_pairs[i][0]
            parent_2 = parent_pairs[i][1]

            new_population.append(
                [parent_1[0] + alpha_1 * (parent_2[0] - parent_1[0]),
                 parent_1[1] + alpha_1 * (parent_2[1] - parent_1[1])])

        return new_population

    # Мутация популяции
    @staticmethod
    def mutate(population, chance, step):
        for i in range(len(population)):
            for j in range(2):
                val = random.uniform(0, 1)

                if val < chance:
                    population[i][j] += step if val < chance / 2 else -step

        return population

    # Запуск генетического алгоритма
    def run_genetic_algorithm(self, num_persons, min_x, max_x, min_y, max_y, parent_function, selection_function,
                              mutation_chance,
                              mutation_step, num_generations):

        population = self.generate_population(num_persons, min_x, max_x, min_y, max_y)

        for p in population:
            self.array_steps.append([p[0], p[1], rosenbrock_function(p[0], p[1])])

        for gen in range(num_generations):
            parents = parent_function(population)

            children = self.get_intermediate_recombination(parents)
            children = self.mutate(children, mutation_chance, mutation_step)

            population += children
            population = selection_function(num_persons, population)

            new_array_steps = []
            for p in population:
                new_array_steps.append([p[0], p[1], rosenbrock_function(p[0], p[1])])

            self.array_steps.append(new_array_steps)

        mn = rosenbrock_function(population[0][0], population[0][1])
        p = population[0]
        for person in population:
            if rosenbrock_function(person[0], person[1]) < mn:
                p = person
                mn = rosenbrock_function(person[0], person[1])

        return [[p[0], p[1], mn]]

    # Запуск гибридного алгоритма
    def run_hybrid_algorithm(self, num_persons, min_x, max_x, min_y, max_y, parent_function, selection_function,
                             mutation_chance, mutation_step, num_generations, iterations, ep1, ep2):

        population = self.run_genetic_algorithm(num_persons, min_x, max_x, min_y, max_y, parent_function,
                                                selection_function, mutation_chance, mutation_step, num_generations)

        min_population = []
        for item in population:
            min_population.append(quickest_descent.quickest_descent(item[0], item[1], iterations, ep1, ep2))

        min_population.sort(key=lambda a: a[1])
        return population

# Создание объекта класса HybridAlgorithm
hybrid_algorithm = HybridAlgorithm()

# Запуск гибридного алгоритма и вывод результатов
result = hybrid_algorithm.run_hybrid_algorithm(200, -5, 5, -5, 5,
                                               hybrid_algorithm.get_panmixia,
                                               hybrid_algorithm.get_selection_by_truncation,
                                               0.05, 0.1, 5, 100, 0.01, 0.01)
print(result)
# for h in result:
#     print(h)
