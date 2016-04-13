import CryptoArithmetic
import GeneticAlgorithm as GA
import Selection
import copy
import logging
import random
import tracemalloc
import cProfile

# format='%(funcName)s(): %(message)s'

class LogFilter(logging.Filter):
    def filter(self, record):
        if record.funcName is "cyclicCrossover" or "dictCrossover":
            return True
        elif record.funcName is "getExpression":
            return False
        elif record.funcName is "dictMutation":
            return False
        else:
            return True


def debug_execs(population):
    debug_execs.runs += 1
    best = Selection.getBestSpecimen(population)
    if best.fitness == CryptoArithmetic.MAX_VALUE:
        debug_execs.hits += 1
    return debug_execs.hits
debug_execs.hits = 0
debug_execs.runs = 0


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    my_log()

    hits = 0
    for i in range(40):
        CryptoArithmetic.getExpression("send", 9567, "more", 1085, "money", 10652)
        population = CryptoArithmetic.makeSpecimen(40)

        population = GA.init(population)
        best = Selection.getBestSpecimen(population)
        if best.fitness == CryptoArithmetic.MAX_VALUE:
            hits += 1
    print("\n  the GA found the answer {} times in 100!".format(hits))


def AG_padrao(runs:int):
    #logging.basicConfig(level=logging.INFO, format='%(message)s')
    CryptoArithmetic.getExpression("money", "send", "more")

    hits = 0
    for i in range(runs):
        #file = 'ag' + str(i) + '.txt'
        #logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename=file)
        #random.seed(i)

        population = CryptoArithmetic.makeSpecimen(100)

        GA.REINSERTION = Selection.TruncationSelection
        population = GA.init(population, generations=50, birthRate=60, mutationRate=5)
        hits = debug_execs(population)
    print("\n  the GA found the answer {} times in {}!".format(hits, runs))


def AG_pequeno():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename="AG_pequeno.txt", filemode='w')
    my_log()

    CryptoArithmetic.getExpression("money", "send", "more")
    population = CryptoArithmetic.makeSpecimen(10)

    Selection.Tournament.__defaults__ = (2,)
    #GA.SELECT = Selection.Tournament
    population = GA.init(population, generations=10, birthRate=40, mutationRate=10)
    #debug_execs(population)


def my_log():
    filter = LogFilter()
    log = logging.getLogger()
    log.addFilter(filter)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    #tracemalloc.start()

    #cProfile.run('AG_padrao(100)')
    AG_pequeno()
    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics('lineno')

    #print("[ Top 10 ]")
    #for stat in top_stats[:10]:
    #    print(stat)


