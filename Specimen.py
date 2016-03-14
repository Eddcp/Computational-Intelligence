import typing
import math


class Specimen(object):
    Population = []

    def __init__(self, chromosome, fitnessEvalFunction):
        self.chromosome = chromosome
        self.fitnessEvalFunction = fitnessEvalFunction
        self.fitness = fitnessEvalFunction(chromosome)
        self.Population.append(self)

    def evalFitness(self):
        self.fitness = self.fitnessEvalFunction(self.chromosome)

    @staticmethod
    def getBestSpecimen():
        if not Specimen.Population:
            return None
        best = Specimen.Population[0]
        for specimen in Specimen.Population:
            if specimen > best:
                best = specimen
        return best

    def __str__(self):
        s = ""
        s += "Fitness= " + str(self.chromosome)
        s += "\tCapability= " + str(self.fitness)
        return s


    def __lt__(self, other):
        if self.fitness > other.fitness:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.fitness < other.fitness:
            return True
        else:
            return False
