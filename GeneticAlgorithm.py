from Specimen import *
from Selection import *
from Crossover import *
from Mutation import *

from CryptoArithmetic import getWordValue
#from CryptoArithmetic import Terms, Result
import CryptoArithmetic as CA

SELECT = Tournament
CROSSOVER = dictCrossover
REINSERTION = BestsInParentsAndChildren
MUTATION = dictMutation

def init(population:list, populationSize:int=None, generations:int=30, birthRate:int=60, mutationRate:int=5,
         childrenPerParents:int=2) -> list:

    populationSize = populationSize if populationSize else len(population)

    logging.debug('\n   INITIATING GENETIC ALGORITHM\n')
    logging.debug('Population Size: %s', populationSize)
    logging.debug('Number of Generations: %s', generations)
    logging.debug('Crossover Rate: %s%%', birthRate)
    logging.debug('Mutation Rate: %s%%\n', mutationRate)

    mutants = int(math.ceil(populationSize * mutationRate / 100))
    births = int(math.ceil(populationSize * birthRate / 100))

    logging.debug('\n  Initial POPULATION')

    debug(population)

    last_diversity_check = 0
    for time in range(generations):
        children = []
        ancestors = population
        for _ in range(int(births / childrenPerParents)):
            parents = SELECT(population, 2)
            embryos = CROSSOVER(parents[0].chromosome, parents[1].chromosome, childrenPerParents)
            for e in embryos:
                children.append(Specimen(e))

        MUTATION(children, mutants)

        population = REINSERTION(ancestors, children, populationSize)
        logging.debug("***************\n  GENERATION %s", time+1)

        best = getBestSpecimen(population)
        debug(population, best)
        if best.fitness >= Specimen.max_fitness:
            return population

        if (time - last_diversity_check >= 5) and (_population_diversity(population) == 1):
            last_diversity_check = time
            return population


    return population


def debug(population:list, best=None):
    best = best if best else getBestSpecimen(population)

    logging.debug('  POPULATION of %s Specimens', len(population))
    if len(population) > 15:
        print_only_fitness(population)
    else:
        for x in population:
            logging.debug(x)

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

def _population_diversity(population:list) -> int:
    fitness_values = set()
    for ind in population:
        fitness_values.add(ind.fitness)
    return(len(fitness_values))