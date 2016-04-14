import CryptoArithmetic
import GeneticAlgorithm as GA
import Selection
import copy
import logging
import random
import tracemalloc
import cProfile
from Specimen import Specimen
import multiprocessing as mp
import threading as th
from multiprocessing.pool import ThreadPool

# format='%(funcName)s(): %(message)s'

class LogFilter(logging.Filter):
    def filter(self, record):
        if record.funcName is "debug":
            return True
        else:
            return False


def debug_execs(population):
    debug_execs.runs += 1
    best = Selection.getBestSpecimen(population)
    if best.fitness == Specimen.max_fitness:
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


def AG_padrao_serial(runs:int):
    #logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    CryptoArithmetic.getExpression("money", "send", "more")

    hits = 0
    for i in range(runs):
        #file = 'ag' + str(i) + '.txt'
        #logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename=file)
        #random.seed(i)

        population = CryptoArithmetic.makeSpecimen(100)
        population = GA.init(population, generations=50, birthRate=60, mutationRate=5)
        hits = debug_execs(population)
    print("\n  Convergence of {}% !".format((hits/runs)*100))
    print("  the GA found the answer {} times in {}!".format(hits, runs))

def AG_padrao_parallel(runs:int):
    #logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    #my_log()
    CryptoArithmetic.getExpression("money", "send", "more")

    N_process = 7
    hits = 0
    tp = ThreadPool(processes=N_process)

    results = mp.Queue(2*N_process)
    completedTasks = 0

    for i in range(N_process):
        population = CryptoArithmetic.makeSpecimen(100)
        tp.apply_async(GA.init, args= (population,), kwds={'generations':50, 'birthRate':60, 'mutationRate':5 }, callback=results.put)

    while completedTasks < runs:
        res = results.get()
        completedTasks += 1
        GA.debug(res)
        hits = debug_execs(res)

        if completedTasks >= runs:
            break
        population = CryptoArithmetic.makeSpecimen(100)
        tp.apply_async(GA.init, args= (population,), kwds={'generations':50, 'birthRate':60, 'mutationRate':5 }, callback=results.put)
    tp.terminate()
    print("\n  Convergence of {}% !".format((hits/runs)*100))
    print("  the GA found the answer {} times in {}!".format(hits, runs))



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

    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    #tracemalloc.start()

    #cProfile.run('AG_padrao(100)')
    AG_padrao_parallel(10)
    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics('lineno')

    #print("[ Top 10 ]")
    #for stat in top_stats[:10]:
    #    print(stat)


