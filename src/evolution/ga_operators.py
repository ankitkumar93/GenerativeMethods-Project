import random

'''
Author: Anand Purohit
Filter module to ensure that we only consider those tweets
that possess a score that is greater than a threshold score
'''
class GAOperators:
    def __init__(self, args):
        # The length of each individual's tag vector
        self.individualLength = args['individualLength']
        # The index in the list of tags on which the child will be split to perform the crossover operation
        self.crossoverPoint = args['crossoverPoint']
        # The probability for a crossover to take place between 2 children
        self.crossoverProbability = args['crossoverProbability']
        # The probability for a mutation to take place on a child
        self.mutationProbability = args['mutationProbability']
        # The number of elites to be selected from each iteration of evolution
        self.numElite = args['numElite']
        # The target population against which the fitness of each individual will be compared
        self.goalPopulation = args['goalPopulation']

    '''
    Performs a mutation on a list of tags (child).
    Two random tags are chosen from the list of tags, and their positions are swapped
    '''
    def mutate(self, child):
        random.seed(64)
        mutatingTags = random.sample(xrange(len(child['tags'])), 2)
        mutantTags = child['tags'][mutatingTags[0]], child['tags'][mutatingTags[1]]
        child['tags'][mutatingTags[0]] = mutantTags[1]
        child['tags'][mutatingTags[1]] = mutantTags[0]
        child['fitness'] = 0
        return child

    '''
    Performs a crossover between 2 list of tags (children).
    Each child is broken into 2 parts, based on the crossoverPoint
    Part 1 of child 1 is then combined with Part 2 of child 2
    Part 1 of child 2 is then combined with Part 2 of child 1
    '''
    def crossover(self, child1, child2):
        part11 = child1['tags'][:self.crossoverPoint]
        part22 = child2['tags'][(self.individualLength - self.crossoverPoint):]
        part12 = child2['tags'][:(self.individualLength - self.crossoverPoint)]
        part21 = child1['tags'][self.crossoverPoint:]
        return dict(fitness=0, tags=part11.extend(part22)), dict(fitness=0, tags=part12.extend(part21))

    '''
    Computes the fitness value for an individual
    '''
    # def evaluate(self, individual):
    #     # fitness = -1
    #     # for goal in self.goalPopulation:
    #     #     sim = calcSimHash(individual['tags'], goal['tags'])
    #     #     currFitness = sim * goal['lrscore']
    #     #     if currFitness > fitness:
    #     #         fitness = currFitness
    #     # individual['fitness'] = fitness
    #     # return fitness

    '''
    Returns the top numElite number of fittest individuals
    This is done by first sorting the population and then picking up the fittest subset of individuals
    '''
    def select(self, population):
        clones = list(population)
        clones.sort(key=lambda clone: clone['fitness'])
        return clones[:self.numElite]
