# these are Selection functions used in a Genetic Algorithm to, primarily,
# select which individuals are going to procreate. But they can be used any
# time you need a selection system.

import random


# Tournament has a low "Selection Pressure" since you could reasonably choose
# just low fitness individuals to "fight" with each other.
def Tournament(population:list, tour:int=3, quantity:int=2) -> list:
    chosen = random.sample(population, tour)

    for x in chosen:
        print(x)

    betters = []
    for i in range(quantity):
        best = chosen[0]
        for specimen in chosen:
            if specimen > best:
                best = specimen
        betters.append(best)
        chosen.remove(best)
    return betters


# -------------------------
# Roulette has a high "Selection Pressure" because the chance of being chosen
# is directly related to the individual's fitness.


# This is a bad implementation because the size of roulette is proportional to
# the range of fitness. In a problem where fitness can have a pretty high value,
# the roulette's size becomes impracticable.
def BadRoulette(population:list, quantity:int=2) -> list:
    roulette = []
    for specimen in population:
        roulette.extend([specimen] * specimen.fitness)

    chosen = random.sample(roulette, quantity)
    return chosen


# This is a better implementation of the Roulette Selection because roulette's size
# depends only on the number of individuals.
def GoodRoulette(population:list, quantity:int=2) -> list:
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


