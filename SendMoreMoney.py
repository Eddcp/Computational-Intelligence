import CryptoArithmetic
import GeneticAlgorithm as GA
import Selection
import copy
import logging
import random

# format='%(funcName)s(): %(message)s'

class LogFilter(logging.Filter):
    def filter(self, record):
        if record.funcName is "cyclicCrossover":
            return False
        elif record.funcName is "getExpression":
            return False
        elif record.funcName is "dictMutation":
            return False
        else:
            return True


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    my_log()

    hits = 0
    for i in range(40):
        CryptoArithmetic.getExpression("send", 9567, "more", 1085, "money", 10652)
        population = CryptoArithmetic.makeSpecimen(40)
        logging.debug('\n\tINITIAL POPULATION')
        GA.debug(population)

        population = GA.init(population)
        best = Selection.getBestSpecimen(population)
        if best.fitness == CryptoArithmetic.MAX_VALUE:
            hits += 1
    print("\n  the GA found the answer {} times in 100!".format(hits))


def AG_padrao():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename='logs/oi.txt')
    CryptoArithmetic.getExpression("send", 9567, "more", 1085, "money", 10652)

    hits = 0
    for i in range(50):
        #file = 'ag' + str(i) + '.txt'
        #logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename=file)
        #random.seed(i)

        population = CryptoArithmetic.makeSpecimen(100)

        GA.REINSERTION = Selection.TruncationSelection
        population = GA.init(population, generations=30, birthRate=60, mutationRate=5)
        best = Selection.getBestSpecimen(population)
        if best == CryptoArithmetic.MAX_VALUE:
            hits += 1
    print("\n  the GA found the answer {} times in 100!".format(hits))


def AG_pequeno():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    my_log()

    CryptoArithmetic.getExpression("send", 9567, "more", 1085, "money", 10652)
    population = CryptoArithmetic.makeSpecimen(10)
    logging.debug('\n\tINITIAL POPULATION')
    GA.debug(population)

    Selection.Tournament.__defaults__ = (2,)
    #GA.SELECT = Selection.Tournament
    GA.REINSERTION = Selection.TruncationSelection
    population = GA.init(population, generations=10, birthRate=40, mutationRate=10)


def my_log():
    filter = LogFilter()
    log = logging.getLogger()
    log.addFilter(filter)


if __name__ == "__main__":
    main()


