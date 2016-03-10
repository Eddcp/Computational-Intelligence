import random


def Tournament(population:list, tour:int=3, quantity:int=2):
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


def Roulette(population:list, quantity:int=2):
    roulette = []
    for specimen in population:
        roulette.extend([specimen] * specimen.fitness)

    chosen = []
    for i in range(quantity):
        chosen.append(random.choice(roulette))
    return chosen
