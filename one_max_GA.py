import random


def randTrueFalse():
    '''Returns ether True or False uniformly at random'''
    if random.randint(0, 1) == 1:
        return True
    else:
        return False

        
def weighted_choice(elements, weights):
    value = random.randint(0, sum(weights) - 1)
    # Loop for each element
    for i in range(len(elements)):
        # Test
        if value < weights[i]:
            return elements[i]
        else:
            value -= weights[i]
            
        

        
        
class one_max_GA:
    '''Performs the 1-max problem optimisation with a genetic algorithm'''

    def __init__(self, chromosome_length, population_size, mutation_rate):
        '''Assigns member variables'''
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate   
        self.next_population = []

    def starting_population(self):
        '''Creates a randomised starting population'''
        self.population = [[randTrueFalse() for y in range(self.chromosome_length)] for x in range(self.population_size)]
        self.fitness = self.measure_fitness()
        
    def measure_fitness(self):
        '''Measures the fitness of each element in the population.
        In this case this means how many True values it contains.'''
        return [self.population[i].count(True)+1 for i in range(self.population_size)]
        
    def crossover(self, mother, father):
        '''Takes in two parents, performs a crossover operation
        and returns a list of a child and the contrapositive child'''
        split_point = random.randint(0, self.population_size-1)
        child = mother[:split_point] + father[split_point:]
        other_child = mother[split_point:] + father[:split_point]
        return (child, other_child)
        
    def create_children(self):
        mother = weighted_choice(self.population, self.fitness)
        father = weighted_choice(self.population, self.fitness)
        children = self.crossover(mother, father)
        self.next_population += children
        
    def cull(self):
        self.population = self.next_population
        self.next_population = []
        self.fitness = self.measure_fitness()
        
    def do_generation(self):
        while len(self.next_population) < self.population_size:
            self.create_children()
        self.cull()
        
if __name__ == "__main__":
    GA = one_max_GA(5, 4, 0.25)
    GA.starting_population()
    #print GA.measure_fitness()
    #print weighted_choice(GA.population, GA.measure_fitness())
    for i in range(10):
        print "At generation " + str(i)
        print "Average fitness is " + str(sum(GA.fitness) / float(len(GA.fitness)))
        #print GA.population
        GA.do_generation()
        