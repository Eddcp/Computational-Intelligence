# these are Selection functions used in a Genetic Algorithm to, primarily,
# select which individuals are going to procreate. But they can be used any
# time you need a selection system.


import random


# Tournament has a low "Selection Pressure" since you could reasonably choose
# just low fitness individuals to "fight" with each other.
def Tournament(population:list, tour:int=3, quantity:int=2) -> list:
    chosen = []
    for i in range(tour):
        choice = random.choice(population)
        while choice in chosen:
            choice = random.choice(population)
        chosen.append(choice)

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


# Roulette has a high "Selection Pressure" because the chance of being chosen
# is directly related to the individual's fitness.
def Roulette(population:list, quantity:int=2) -> list:
    roulette = []
    for specimen in population:
        roulette.extend([specimen] * specimen.fitness)

    chosen = []
    for i in range(quantity):
        chosen.append(random.choice(roulette))
    return chosen
