#TODO checar se a forma que estou calculando a mutacao esta correta.
# atualmente, estou pegando TAXA_MUTACAO% da populacao e aplicando a mutacao.
# meu medo eh fazendo isso, estou deixando o alg muito deterministico
import random
import logging
from Specimen import Specimen
from CryptoArithmetic import evalFitness



def dictMutation(population:list, quantity:int):
    chosen = random.sample(population, quantity)
    logging.debug('  {} MUTATIONS'.format(quantity))
    for ind in chosen:
        assert isinstance(ind, Specimen)
        logging.debug("Before:         {}".format(ind))
        letterA, letterB = random.sample(ind.chromosome.keys(), 2)
        aux = ind.chromosome[letterA]
        ind.chromosome[letterA] = ind.chromosome[letterB]
        ind.chromosome[letterB] = aux
        ind.evalFitness()
        logging.debug("After {} <-> {} : {}\n".format(letterA, letterB, ind))




