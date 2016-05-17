# these are Selection functions used in a Genetic Algorithm to, primarily,
# select which individuals are going to procreate. But they can be used any
# time you need a selection method.

import random
import math

# Tournament has a low "Selection Pressure" since you could reasonably choose
# just low fitness individuals to "fight" with each other.
class Tournament:
    def __init__(self, tour:int):
        self.tour = tour

    def run(self, population:list, quantity:int) -> list:
        ''' Tournament '''
        betters = []
        for _ in range(quantity):
            chosen = []
            for _ in range(self.tour):
                chosen.append(random.choice(population))
            best = getBestSpecimen(chosen)
            betters.append(best)
        return betters

    def __str__(self):
        return 'Tournament {}'.format(self.tour)


# -------------------------
# Roulette has a high "Selection Pressure" because the chance of being chosen
# is directly related to the individual's fitness.


# This is a bad implementation because the size of roulette is proportional to
# the range of fitness. In a problem where fitness can have a pretty high value,
# the roulette's size becomes impracticable.
def BadRoulette(population:list, quantity:int) -> list:
    ''' BadRoulette '''
    roulette = []
    for specimen in population:
        roulette.extend([specimen] * specimen.fitness)

    chosen = random.sample(roulette, quantity)
    return chosen


# This is a better implementation of the Roulette Selection because roulette's size
# depends only on the number of individuals.
def GoodRoulette(population:list, quantity:int) -> list:
    ''' GoodRoulette '''
    roulette = []
    summation = 0
    for specimen in population:
        summation += specimen.fitness
        roulette.append((summation, specimen))

    chosen = []
    for i in range(quantity):
        while True:
            randFit = random.randrange(0, summation)
            for tup in roulette:
                if tup[0] > randFit:
                    choice = tup[1]
                    break
            if choice not in chosen:
                chosen.append(choice)
                break

    return chosen


def TruncationSelection(population:list, quantity:int) -> list:
    new_pop = sorted(population, reverse=True)
    return new_pop[:quantity]



def getBestSpecimen(population:list):
    best = population[0]
    for specimen in population:
        if specimen > best:
            best = specimen
    return best

def getWorstSpecimen(population:list):
    worst = population[0]
    for specimen in population:
        if specimen < worst:
            worst = specimen
    return worst


def BestsInParentsAndChildren(parents:list, children:list, quantity:int) -> list:
    ''' BestsInParentsAndChildren '''
    population = parents + children
    return TruncationSelection(population, quantity)


def Elitism(parents:list, children:list, quantity:int, elitismRate:int=20) -> list:
    ''' Elitism '''
    elite_size = int((quantity * elitismRate)/100)
    parents = TruncationSelection(parents, elite_size)
    children_size = quantity - elite_size
    children = random.sample(children, children_size)
    return parents + children

