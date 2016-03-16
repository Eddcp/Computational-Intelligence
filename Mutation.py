#TODO checar se a forma que estou calculando a mutacao esta correta.
# atualmente, estou pegando TAXA_MUTACAO% da populacao e aplicando a mutacao.
# meu medo eh fazendo isso, estou deixando o alg muito deterministico
import random
import logging
from Specimen import Specimen
from CryptoArithmetic import evalFitness



def makeMutation(population:list, rate:int):
    rate /= 100
    chosen = random.sample(population, int(rate * len(population)) )

    for ind in chosen:
        assert isinstance(ind, Specimen)
        logging.debug("Before Mutation:  {}".format(ind))
        letterA, letterB = random.sample(ind.chromosome.keys(), 2)
        aux = ind.chromosome[letterA]
        ind.chromosome[letterA] = ind.chromosome[letterB]
        ind.chromosome[letterB] = aux
        ind.evalFitness()
        logging.debug("After Mutation:   {}".format(ind))




