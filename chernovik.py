def select(self):
    sorted_pop = sorted(self.population, key=lambda item: item[2], reverse=not self.min_func)
    cutoff = int(self.pop_number * self.survive_cof)
    parents1 = sorted_pop[cutoff:2 * cutoff]
    parents2 = sorted_pop[self.pop_number - cutoff:self.pop_number]

    children = []
    for i in range(self.pop_number - cutoff):
        parent1 = parents1[i % len(parents1)]
        parent2 = parents2[i % len(parents2)]
        if random() > 0.5:
            child = [parent1[0], parent2[1], self.func(parent1[0], parent2[1])]
        else:
            child = [parent2[0], parent1[1], self.func(parent2[0], parent1[1])]
        children.append(child)

    self.population = sorted_pop[:cutoff] + children


    #получили новую популяцию, потом отсортировали популяцию и оставили только хороших


#  версия где работает лучше но не то что надо

    def select(self):
        sorted_pop = sorted(self.population, key=lambda item: item[2], reverse=not self.min_func)
        cutoff = int(self.pop_number * self.survive_cof) #выбираем лучших особей
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


