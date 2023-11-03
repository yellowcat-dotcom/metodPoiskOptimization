from random import uniform, random


class GeneticAlgorithmL3:
    def __init__(self, func, generations=50, min=True, mut_chance=0.2, survive_cof=0.8, pop_number=20):
        self.func = func
        self.population = []
        self.mut_chance = mut_chance
        self.survive_cof = survive_cof
        self.generations = generations
        self.pop_number = pop_number
        self.min_func = min

    def generate_start_population(self, x, y):
        for _ in range(self.pop_number):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.population.append([po_x, po_y, self.func(po_x, po_y)])

    def statistic(self):
        if self.min_func:
            min_individual = min(self.population, key=lambda item: item[2])
            return min_individual[0], min_individual[1], min_individual[2]

    def select(self):
        sorted_pop = sorted(self.population, key=lambda item: item[2], reverse=not self.min_func)
        cutoff = int(self.pop_number * self.survive_cof)  # выбираем лучших особей
        elite = sorted_pop[:cutoff]
        parents1 = elite
        parents2 = elite

        children = []
        for i in range(self.pop_number - cutoff):
            parent1 = parents1[i % len(parents1)]
            parent2 = parents2[i % len(parents2)]
            if random() > 0.5:
                child = [parent1[0], parent2[1], self.func(parent1[0], parent2[1])]
            else:
                child = [parent2[0], parent1[1], self.func(parent2[0], parent1[1])]
            children.append(child)

        self.population = elite + children

    def mutation(self, cur_gen):
        sorted_pop = sorted(self.population, key=lambda item: item[2], reverse=self.min_func)
        for i in range(len(sorted_pop)):
            if random() < self.mut_chance:
                sorted_pop[i][0] += (random() - self.mut_chance) * ((self.generations - cur_gen) / self.generations)
            if random() < self.mut_chance:
                sorted_pop[i][1] += (random() - self.mut_chance) * ((self.generations - cur_gen) / self.generations)
            sorted_pop[i][2] = self.func(sorted_pop[i][0], sorted_pop[i][1])

        self.population = sorted_pop