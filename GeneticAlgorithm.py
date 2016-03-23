from Specimen import *
from Selection import *
from Crossover import *
from Mutation import *

from CryptoArithmetic import getWordValue

SELECT = Tournament
CROSSOVER = cyclicCrossover
REINSERTION = TruncationSelection
MUTATION = dictMutation

def init(population:list, populationSize:int=None, generations:int=30, birthRate:int=60, mutationRate:int=5,
         childrenPerParents:int=1) -> list:

    populationSize = populationSize if populationSize else len(population)
    xmen = int(math.ceil(populationSize * mutationRate / 100))
    births = int(math.ceil(populationSize * birthRate / 100))

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

        logging.debug("***************\n  GENERATION {}".format(time+1))
        debug(population) if logging.DEBUG else None

    return population

def debug(population:list):
    logging.debug('  POPULATION of {} Specimens'.format(len(population)))
    if len(population) > 15:
        print_only_fitness(population)
    else:
        for x in population:
            logging.debug(x)

    #best = getBestSpecimen(population)
    best = population[0]
    logging.debug("\n\t* THE BEST *\n{}".format(best))
    send = getWordValue(best.chromosome, "send")
    more = getWordValue(best.chromosome, "more")
    money = getWordValue(best.chromosome, "money")
    logging.debug("SEND = {}, MORE = {}, MONEY = {}".format(send, more, money))
    logging.debug("SEND + MORE = {}".format(send + more))
    logging.debug('(SEND + MORE) - MONEY = {}'.format(abs(send + more - money)))
    # logging.debug("Real Capability = {}".format(abs(send + more - 10652)))
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