import random
import logging
from Specimen import Specimen
logging.basicConfig(level=logging.DEBUG, format='%(funcName)s(): %(message)s')



def makeMutation(population:list, rate:int):
    rate /= 100
    chosen = random.sample(population, int(rate * len(population)) )

    for ind in chosen:
        assert isinstance(ind, Specimen)
        logging.debug("Before Mutation: {}".format(ind))
        letterA, letterB = random.sample(ind.chromosome.keys(), 2)
        aux = ind.chromosome[letterA]
        ind.chromosome[letterA] = ind.chromosome[letterB]
        ind.chromosome[letterB] = aux
        ind.evalFitness()
        logging.debug("After Mutation: {}".format(ind))

