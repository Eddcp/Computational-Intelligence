from Specimen import *
from Selection import *
from Crossover import *
from Mutation import *

from CryptoArithmetic import getWordValue
#from CryptoArithmetic import Terms, Result
import CryptoArithmetic as CA

SELECT = Tournament(3).run
CROSSOVER = DictCrossover(cyclicCrossover).run
REINSERTION = Elitism
MUTATION = dictMutation

def init(population:list, populationSize:int=None, num_generations:int=30, birthRate:int=60, mutationRate:int=5,
         childrenPerParents:int=2) -> dict:

    populationSize = populationSize if populationSize else len(population)

    if init.first_time:
        init.first_time = False
        logging.info('\n   PROPERTIES')
        logging.info('Population Size: %s', populationSize)
        logging.info('Number of Generations: %s', num_generations)
        logging.info('Crossover Rate: %s%%', birthRate)
        logging.info('Mutation Rate: %s%%\n', mutationRate)

        # logging.info('   METHODS')
        # logging.info('Selection: %s', SELECT.__name__)
        # logging.info('Crossover: %s', CROSSOVER.__name__)
        # logging.info('Reinsertion: %s\n', REINSERTION.__name__)
        #SELECT.__te


    mutants = int(math.ceil(populationSize * mutationRate / 100))
    births = int(math.ceil(populationSize * birthRate / 100))

    logging.debug('\n  Initial POPULATION')

    debug(population)

    last_diversity_check = 0
    generation = 0
    best = None
    for generation in range(1, num_generations+1):
        children = []
        ancestors = population
        for _ in range(math.ceil(births / childrenPerParents)):
            parents = SELECT(population, 2)
            embryos = CROSSOVER(parents[0].chromosome, parents[1].chromosome, childrenPerParents)
            for e in embryos:
                children.append(Specimen(e))

        MUTATION(children, mutants)

        population = REINSERTION(ancestors, children, populationSize)
        logging.debug("***************\n  GENERATION %s", generation)

        best = getBestSpecimen(population)
        debug(population, best)
        if best.fitness >= Specimen.max_fitness:
            break

        if (generation - last_diversity_check >= 5) and (_population_diversity(population) == 1):
            last_diversity_check = generation
            break

    return {'population':population, 'generation':generation, 'best':best}
init.first_time = True

def debug(population:list, best=None):
    best = best if best else getWorstSpecimen(population)

    logging.debug('  POPULATION of %s Specimens', len(population))
    if len(population) > 15:
        print_only_fitness(population)
    else:
        for x in population:
            logging.debug(x)

    logging.debug("\n\t* THE BEST *\n%s", best)
    logging.debug(CA.CA_str_values(best.chromosome))
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


def StandardGA(population:list):

    population_size = 100
    max_generation = 50
    crossover_rate = 80
    mutation_rate = 10

    #assert(len(population) == population_size)

    return (init(population, populationSize=population_size, num_generations=max_generation, birthRate=crossover_rate, mutationRate=mutation_rate))



