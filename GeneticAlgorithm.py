from Specimen import *
from Selection import *
from Crossover import *
from Mutation import *

from CryptoArithmetic import getWordValue

SELECT = GoodRoulette
CROSSOVER = cyclicCrossover
REINSERTION = TruncationSelection
MUTATION = dictMutation

def init(population:list, populationSize:int=None, generations:int=30, birthRate:int=60, mutationRate:int=5,
         childrenPerParents:int=1) -> list:

    populationSize = populationSize if populationSize else len(population)


    logging.debug('\n   INITIATING GENETIC ALGORITHM\n')
    logging.debug('Population Size: %s', populationSize)
    logging.debug('Number of Generations: %s', generations)
    logging.debug('Crossover Rate: %s%%', birthRate)
    logging.debug('Mutation Rate: %s%%\n', mutationRate)

    xmen = int(math.ceil(populationSize * mutationRate / 100))
    births = int(math.ceil(populationSize * birthRate / 100))

    logging.debug('\n  Initial POPULATION')
    debug(population)

    for time in range(generations):
        children = []
        for _ in range(int(births / childrenPerParents)):
            parents = SELECT(population, 2)
            embryos = CROSSOVER(parents[0].chromosome, parents[1].chromosome, childrenPerParents)
            for e in embryos:
                children.append(Specimen(e))
        MUTATION(children, xmen)
        population.extend(children)

        population = REINSERTION(population, populationSize)

        logging.debug("***************\n  GENERATION %s", time+1)
        debug(population) if logging.DEBUG else None

    return population

def debug(population:list):
    logging.debug('  POPULATION of %s Specimens', len(population))
    if len(population) > 15:
        print_only_fitness(population)
    else:
        for x in population:
            logging.debug(x)

    best = getBestSpecimen(population)
    logging.debug("\n\t* THE BEST *\n%s", best)
    send = getWordValue(best.chromosome, "send")
    more = getWordValue(best.chromosome, "more")
    money = getWordValue(best.chromosome, "money")
    logging.debug("SEND = %s, MORE = %s, MONEY = %s", send, more, money)
    logging.debug("SEND + MORE = %s", send + more)
    logging.debug('(SEND + MORE) - MONEY = %s', abs(send + more - money))
    # logging.debug("Real Capability = %s", abs(send + more - 10652)))
    logging.debug("****************\n")


def print_only_fitness(population:list):
    c = 0
    s = "\n"
    for x in population:
        s += str(x.fitness) + " "
        if c == 10:
            s += "\n"
            c = -1
        c+=1
    logging.debug(s)