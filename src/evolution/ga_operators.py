import random

from simhash import Simhash

'''
Author: Anand Purohit
Module to define the different operators to be used in the genetic algorithm
'''
class GAOperators:
    def __init__(self, args):
        self.logger = args['logger']
        # The length of each individual's tag vector
        self.individualLength = args['individualLength']
        # The probability for a crossover to take place between 2 children
        self.crossoverProbability = args['crossoverProbability']
        # The probability for a mutation to take place on a child
        self.mutationProbability = args['mutationProbability']
        # The number of elites to be selected from each iteration of evolution
        self.numElite = args['numElite']
        # The hash bit length
        self.hashLength = 64
        # Set Random
        # Selection
        self.rcs = random.Random(500)
        self.rms = random.Random(500)

        # Probability
        self.rcp = random.Random(500)
        self.rmp = random.Random(500)

    '''
    Set the goal population for the genetic algorithm.
    '''
    def set_goal_population(self, goalPopulation):
        # The target population against which the fitness of each individual will be compared
        self.goalPopulation = goalPopulation

    '''
    Performs a mutation on a list of tags (child).
    Two random tags are chosen from the list of tags, and their positions are swapped
    '''
    def mutate(self, child):
        if self.rmp.random() < self.mutationProbability:
            mutatingTag1 = self.rms.randint(0, len(child['tags']) - 1)
            mutatingTag2 = self.rms.randint(0, len(child['tags']) - 1)
            mutantTags = [child['tags'][mutatingTag1], child['tags'][mutatingTag2]]
            child['tags'][mutatingTag1] = mutantTags[1]
            child['tags'][mutatingTag2] = mutantTags[0]
            child['fitness'] = 0
            # self.logger.debug("Mutation Successful!")
        return child

    '''
    Performs a crossover between 2 list of tags (children).
    Each child is broken into 2 parts, based on the crossoverPoint
    Part 1 of child 1 is then combined with Part 2 of child 2
    Part 1 of child 2 is then combined with Part 2 of child 1
    '''
    def crossover(self, child1, child2):
        indexRange = min(len(child1['tags']), len(child2['tags']))
        crossoverPoint = self.rcs.randint(0, indexRange - 1)
        if self.rcp.random() < self.crossoverProbability:
            part11 = child1['tags'][:crossoverPoint]
            part22 = child2['tags'][crossoverPoint:]
            part12 = child2['tags'][:crossoverPoint]
            part21 = child1['tags'][crossoverPoint:]

            child1Tags = part11 + part22
            child2Tags = part12 + part21
            if child1Tags.count("NNP") is 1 and child2Tags.count("NNP") is 1\
                    and child1Tags.count("JJ") >= 1 and child2Tags.count("JJ") >= 1:
                # self.logger.debug("Crossover Successful!")
                return dict(fitness=0, tags=child1Tags), dict(fitness=0, tags=child2Tags)
        return dict(fitness=0, tags=list(child1['tags'])), dict(fitness=0, tags=list(child2['tags']))

    '''
    Computes the fitness value for an individual
    '''
    def evaluate(self, individual):
        fitness = -1
        for goal in self.goalPopulation:
            sim = Simhash(" ".join(individual['tags'])).distance(Simhash(" ".join(goal['tags'])))
            currFitness = (1-sim/float(self.hashLength)) * goal['lrscore']
            if currFitness > fitness:
                fitness = currFitness
        individual['fitness'] = fitness
        return fitness

    '''
    Returns the top numElite number of fittest individuals
    This is done by first sorting the population and then picking up the fittest subset of individuals
    '''
    def select(self, population):
        clones = list(population)
        clones.sort(key=lambda clone: clone['fitness'], reverse=True)
        return clones[:self.numElite]

