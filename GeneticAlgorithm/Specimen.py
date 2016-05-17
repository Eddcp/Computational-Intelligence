import typing
import math


class Specimen(object):
    fitnessEvalFunction = None
    max_fitness = 0

    def __init__(self, chromosome):
        assert self.fitnessEvalFunction, "Set Fitness Evaluation Function first!"
        self.chromosome = chromosome
        self.fitness = Specimen.fitnessEvalFunction(self.chromosome)

    def evalFitness(self):
        self.fitness = Specimen.fitnessEvalFunction(self.chromosome)

    @staticmethod
    def setFitnessEvalFunction(func):
        Specimen.fitnessEvalFunction = func

    def __str__(self):
        s = "Chromosome={}  Fitness={}".format(self.chromosome, self.fitness)
        return s


    def __lt__(self, other):
        if self.fitness < other.fitness:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.fitness > other.fitness:
            return True
        else:
            return False


