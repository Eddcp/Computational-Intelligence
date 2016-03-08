import typing
import math


class Specimen(object):
    Population = []

    def __init__(self, feature, capabilityFunction):
        self.feature = feature
        self.capability = capabilityFunction(feature)
        self.Population.append(self)

    @staticmethod
    def getBestSpecimen():
        if not Specimen.Population:
            return None
        best = Specimen.Population[0]
        for specimen in Specimen.Population:
            if specimen.capability < best.capability:
                best = specimen
        return best
