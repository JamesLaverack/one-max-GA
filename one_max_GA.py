import random


def weighted_choice(elements, weights):
    '''Picks a value from a list of elements, weighted by a list of weights.
    Such that the element 'elements[i]' has weighting 'weights[i]'. It is
    assumed that the weightings are integers and are not normalised.'''
    value = random.randint(0, sum(weights) - 1)
    # Loop for each element
    for i in range(len(elements)):
        # Test
        if value < weights[i]:
            return elements[i]
        else:
            value -= weights[i]


def average(L):
    '''Returns the floating-point average of all the values in a list'''
    return sum(L) / float(len(L))


class OneMaxGA:
    '''Performs the 1-max problem optimisation with a genetic algorithm'''

    def __init__(self, chromosome_length, population_size, mutation_rate):
        '''Assigns member variables'''
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.next_population = []

    def starting_population(self):
        '''Creates a randomised starting population'''
        self.population = [[random.choice([True, False])
        for y in range(self.chromosome_length)]
        for x in range(self.population_size)]
        self.fitness = self.measure_fitness()

    def measure_fitness(self):
        '''Measures the fitness of each element in the population.
        In this case this means how many True values it contains.'''
        return [self.population[i].count(True) + 1
        for i in range(self.population_size)]

    def mutate(self, element):
        '''Takes a single element and mutates it.'''
        for i in range(len(element)):
            if random.random() < self.mutation_rate:
                # mutate this gene!
                element[i] = not(element[i])
        return element

    def crossover(self, mother, father):
        '''Takes in two parents, performs a crossover operation
        and returns a list of a child and the contrapositive child'''
        split_point = random.randint(0, self.chromosome_length - 1)
        child = mother[:split_point] + father[split_point:]
        other_child = mother[split_point:] + father[:split_point]
        return (child, other_child)

    def create_children(self):
        '''Gets two random parents and creates two children from this'''
        mother = weighted_choice(self.population, self.fitness)
        father = weighted_choice(self.population, self.fitness)
        children = self.crossover(mother, father)
        self.next_population += [self.mutate(children[0])]
        self.next_population += [self.mutate(children[1])]

    def cull(self):
        '''Kills off the last population and moves onto the next.'''
        self.population = self.next_population
        self.next_population = []
        self.fitness = self.measure_fitness()

    def do_generation(self):
        '''Performs an entire generation, including creating children and
        culling the previous generation.'''
        while len(self.next_population) < self.population_size:
            self.create_children()
        self.cull()

if __name__ == "__main__":
    GA = OneMaxGA(5, 4, 0.25)
    GA.starting_population()
    for i in range(10):
        print "At generation " + str(i) + " average fitness is " + str(
        average(GA.fitness))
        GA.do_generation()
