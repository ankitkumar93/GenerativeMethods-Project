from apis.db import DBHelper
from ga_operators import GAOperators
import json
import random

'''
Author: Ankit Kumar
Genetic Algorithm: Defines the Genetic Algorithm
'''

class GeneticAlgorithm:
    def __init__(self, args):
        self.logger = args['logger']
        config = json.load(open(args['ga_path']))
        self.gaoperators = GAOperators(dict(logger=args['logger'],
                                            individualLength=config['individual_length'],
                                            crossoverPoint=config['crossover_point'],
                                            crossoverProbability=config['crossover_probability'],
                                            mutationProbability=config['mutation_probability'],
                                            numElite=config['num_elite']))
        self.lrThreshold = config['lr_threshold']
        self.maxFitness = config['max_fitness']
        self.maxIterations = config['max_iterations']
        self.populationSize = config['population_size']
        self.goalPopulationSize = args['goal_population_size']
        self.numElite = config['num_elite']

        self.db = DBHelper(dict(logger=args['logger']))

    def generate_population(self):
        data = self.db.get_filtered_tweets()
        random.shuffle(data)
        selectedData = data[:self.populationSize]
        self.population = [dict(tags=x['tags'], fitness=0) for x in selectedData]

    def generate_goal_population(self):
        data = self.db.get_filtered_tweets_condition(self.lrThreshold)
        random.shuffle(data)
        selectedData = data[:self.goalPopulationSize]
        goalPopulation = [dict(tags=x['tags'], lrscore=x['lrscore']) for x in selectedData]
        self.gaoperators.set_goal_population(goalPopulation)

    def evolve(self):
        for gen in range(self.maxIterations):
#            self.logger.debug("Generations: %d" % gen)

            # Compute Fitness
            generationMaxFitness = 0
            for individual in self.population:
                self.gaoperators.evaluate(individual)

            fittestChild = max(self.population, key=lambda child: child['fitness'])
            if fittestChild['fitness'] >= self.maxFitness:
                break

            self.logger.debug("Fitness: %f" % fittestChild['fitness'])

            # Generate Offsprings
            # Select Elites
            offsprings = self.gaoperators.select(self.population)
 
            # CrossOver
            remainingOffsprings = self.populationSize - self.numElite
            r = random.Random(500)
            while remainingOffsprings > 0:
                    childIndex1 = 0
                    childIndex2 = 0
                    while childIndex1 == childIndex2:
                        childIndex1 = r.randint(0, self.numElite - 1)
                        childIndex2 = r.randint(0, self.numElite - 1)
                    
                    child1 = offsprings[childIndex1]
                    child2 = offsprings[childIndex2]

                    offspring1 , offspring2 = self.gaoperators.crossover(child1, child2)
                    offsprings.append(offspring1)
                    offsprings.append(offspring2)
                    
                    remainingOffsprings -= 2

            # fittestChild = max(offsprings, key=lambda child: child['fitness'])
            # self.logger.debug("Fitness after Crossover: %f" % fittestChild['fitness'])
            # Mutation
            for childIndex in xrange(self.numElite, self.populationSize):
                child = offsprings[childIndex]
                self.gaoperators.mutate(child)


            # fittestChild = max(offsprings, key=lambda child: child['fitness'])
            # self.logger.debug("Fitness after Mutation: %f" % fittestChild['fitness'])
            
            # Set Population to new Generation
            self.population = offsprings

        solution = max(self.population, key=lambda child: child['fitness'])
        return solution
