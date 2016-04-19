import CryptoArithmetic
import GeneticAlgorithm as GA
import Selection
import Crossover
import copy
import logging
import timeit
import time
import random
import tracemalloc
import cProfile
from Specimen import Specimen
import multiprocessing as mp
import threading as th
from multiprocessing.pool import ThreadPool
import re

# format='%(funcName)s(): %(message)s'

class LogFilter(logging.Filter):
    def filter(self, record):
        if record.funcName is "debug":
            return True
        else:
            return False


class DebugExecutions:
    def __init__(self):
        self.hits = 0
        self.runs = 0
        self.generations = []
        self.generation = 0
        
    def inspect(self, GA_result:dict):
        best = GA_result['best']
        generation = GA_result['generation']
        self.runs += 1
        self.generations.append(generation)
        self.generation = round(sum(self.generations) / len(self.generations))
        if best.fitness >= Specimen.max_fitness:
            self.hits += 1
            return best
        return None


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
        population = GA.init(population, num_generations=50, birthRate=60, mutationRate=5)
        hits = debug_execs(population)
    print("\n  Convergence of {}% !".format((hits/runs)*100))
    print("  the GA found the answer {} times in {}!".format(hits, runs))




def parallel_run(runs:int):
    #logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    #my_log()

    solutions = []
    N_process = 7
    hits = 0
    tp = ThreadPool(processes=N_process)

    results = mp.Queue(2*N_process)
    completedTasks = 0

    debug = DebugExecutions()

    for i in range(min(N_process, runs)):
        population = CryptoArithmetic.makeSpecimen(100)
        tp.apply_async(GA.StandardGA, args= (population,), callback=results.put)

    while completedTasks < runs:
        res = results.get()
        completedTasks += 1
        GA.debug(res['population'], res['best'])
        solution = debug.inspect(res)
        if solution:
            solutions.append(solution)

        if completedTasks >= runs:
            break
        population = CryptoArithmetic.makeSpecimen(100)
        tp.apply_async(GA.StandardGA, args= (population,), callback=results.put)
    tp.close()
    tp.terminate()

    hits = debug.hits
    hits_rate = round((hits/runs)*100, 2)
    logging.info("   CONVERGENCE of {}% ; {} times in {}!".format(hits_rate, hits, runs))
    logging.info("   Needed, in general, {} Generations.".format(debug.generation))
    for s in solutions:
        logging.debug(s)
        logging.debug(CryptoArithmetic.CA_str_values(s.chromosome))
    #GA.init.first_time = True


def AG_pequeno():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename="AG_pequeno.txt", filemode='w')
    #my_log()

    CryptoArithmetic.getExpression("robert", "donald", "gerald")
    #CryptoArithmetic.getExpression("money", "send", "more")
    population = CryptoArithmetic.makeSpecimen(10)

    Selection.Tournament.__defaults__ = (2,)
    #GA.SELECT = Selection.Tournament
    population, generation, best = GA.init(population, num_generations=10, birthRate=40, mutationRate=10)
    #debug_execs(population)


def permute_methods(runs:int):
    tour2 = Selection.Tournament(2)
    tour3 = Selection.Tournament(3)
    cyclic = Crossover.DictCrossover(Crossover.cyclicCrossover)
    pmx = Crossover.DictCrossover(Crossover.PMX)

    selections = [Selection.GoodRoulette, tour2.run, tour3.run]
    crossovers = [cyclic.run, pmx.run]
    reinsertions = [Selection.BestsInParentsAndChildren, Selection.Elitism]

    for select in selections:
        for crossover in crossovers:
            for reinsertion in reinsertions:
                GA.SELECT = select
                GA.CROSSOVER = crossover
                GA.REINSERTION = reinsertion

                logging.info('   METHODS')
                logging.info('Selection: %s', select.__doc__)
                logging.info('Crossover: %s', ' Cyclic ' if crossover == cyclic.run else ' PMX ')
                logging.info('Reinsertion: %s', reinsertion.__doc__)

                before = time.time()
                parallel_run(runs)
                after = time.time()

                logging.info('TIME: %s\n', round(after - before, 2))


def my_log():
    filter = LogFilter()
    log = logging.getLogger()
    log.addFilter(filter)


def experiment1():

    runs = 1000

    logging.basicConfig(level=logging.INFO, format='%(message)s', filename='experimento1')

    CryptoArithmetic.getExpression("send", "more", result="money")
    logging.info("\n---------------\n\n    SEND + MORE = MONEY\n")
    permute_methods(runs)

    CryptoArithmetic.getExpression("eat", "that", result="apple")
    logging.info("\n---------------\n\n    EAT + THAT = APPLE\n")
    permute_methods(runs)

    CryptoArithmetic.getExpression("cross", "roads", result="danger")
    logging.info("\n---------------\n\n    CROSS + ROADS = DANGER\n")
    permute_methods(runs)

    CryptoArithmetic.getExpression("coca", "cola", result="oasis")
    logging.info("\n---------------\n\n    COCA + COLA = OASIS\n")
    permute_methods(runs)

    CryptoArithmetic.getExpression("donald", "gerald", result="robert")
    logging.info("\n---------------\n\n    DONALD + GERALD = ROBERT\n")
    permute_methods(runs)


def read_results(file):
    re_convergence = '\s*convergence of ([0-9]+\.?[0-9]*)'
    re_time = 'time: ([0-9]+\.?[0-9]*)'
    re_division = '(---)+'

    re_convergence = re.compile(re_convergence)
    re_time = re.compile(re_time)
    re_division = re.compile(re_division)

    problems = []
    convergences = []
    times = []
    for line in file:
        line = line.lower()
        print(line)
        convergence_match = re_convergence.match(line)
        if convergence_match:
            print('BLA!')
            convergences.append(convergence_match.group(1))
        else:
            time_match = re_time.match(line)
            if time_match:
                times.append(time_match.group(1))
            else:
                division_match = re_division.match(line)
                if division_match:
                    problems.append((convergences, times))
                    convergences = []
                    times = []
    #problems = problems[1:]


    print(problems)

    new_file = open(file.name + '-results.txt', mode='w')
    for problem in problems:
        convergences = problem[0]
        times = problem[1]
        for convergence, time in zip(convergences, times):
            new_file.write('{} {}\n'.format(convergence, time))
        new_file.write('\n')






if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, format='%(message)s')
    #CryptoArithmetic.getExpression("cross", "roads", result="danger")
    #CryptoArithmetic.getExpression("eat", "that", result="apple")
    #CryptoArithmetic.getExpression("coca", "cola", result="oasis")
    #CryptoArithmetic.getExpression("donald", "gerald", result="robert")
    #CryptoArithmetic.getExpression("send", "more", result="money")

    file = open('experimento1.txt')
    read_results(file)


    #parallel_run(1000)
    #experiment1()











