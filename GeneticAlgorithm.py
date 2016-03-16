from Specimen import *
from Selection import *
from Crossover import *
from Mutation import *

from CryptoArithmetic import getWordValue



def init(population:list, populationSize:int=None, generations:int=30, birthRate:int=60, mutationRate:int=5,
         childrenPerParents:int=1, selection:str="tournament"):

    populationSize = populationSize if populationSize else len(population)

    if selection.lower() is "roulette":
        select = GoodRoulette
    else:
        select = Tournament

    for time in range(generations):
        logging.debug("\n Generation {}".format(time))
        births = math.ceil(populationSize * birthRate / 100)
        children = []
        for _ in range(births - childrenPerParents):
            parents = select(population, 2)
            embryos = cyclicCrossover(parents[0].chromosome, parents[1].chromosome, childrenPerParents)
            for e in embryos:
                children.append(Specimen(e))
        makeMutation(children, mutationRate)
        population.extend(children)

        population = getTopX(population, populationSize)

        logging.debug(debug(population))


def debug(population:list):
    c = 0
    s = "\n"
    for x in population:
        s += str(x.fitness) + " "
        if c == 10:
            s += "\n"
            c = -1
        c+=1
    logging.debug(s)

    best = getBestSpecimen(population)
    logging.debug("\n\t* THE BEST *\n{}".format(best))
    send = getWordValue(best.chromosome, "send")
    more = getWordValue(best.chromosome, "more")
    money = getWordValue(best.chromosome, "money")
    logging.debug("SEND = {}".format(send))
    logging.debug("MORE = {}".format(more))
    logging.debug("MONEY = {}".format(money))
    logging.debug("SEND + MORE = MONEY ?? {}".format(send + more))
    logging.debug("Real Capability = {}".format(abs(send + more - 10652)))
    logging.debug("****************\n")