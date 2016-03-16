import CryptoArithmetic
import GeneticAlgorithm as GA
import Selection
import copy
import logging


class LogFilter(logging.Filter):
    def filter(self, record):
        if record.funcName is "cyclicCrossover":
            return False
        else:
            return True

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s(): %(message)s')
    filter = LogFilter()
    log = logging.getLogger()
    log.addFilter(filter)
    CryptoArithmetic.getExpression("send", 9567, "more", 1085, "money", 10652)
    population = CryptoArithmetic.makeSpecimen(40)
    GA.debug(population)
    GA.init(population)

    # print("\nOriginal")
    # for x in population:
    #     print (x)
    #
    # print("\nBESTS\n")
    # for y in Selection.getTopX(population, 5):
    #     print(y)


if __name__ == "__main__":
    main()


