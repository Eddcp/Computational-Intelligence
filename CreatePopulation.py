import itertools
import random

import collections
from Specimen import *

NUMBERS = range(10)

Letters = ""
PossibleValues = []

Term = collections.namedtuple("Term", ["word", "value"])
Terms = {}


def init(first, firstValue, second, secondValue, result, resultValue):
    global Letters
    global NUMBERS
    global PossibleValues
    global Terms

    Terms = dict(first=Term(first, firstValue), second=Term(second, secondValue), result=Term(result, resultValue))

    words = [first, second, result]
    for word in words:
        for letter in word:
            if letter in Letters:
                continue
            Letters += letter

    PossibleValues = list(itertools.permutations(NUMBERS, len(Letters)))


def evalCapability(feature):
    global Terms

    localValue = ""
    for letter in Terms["result"].word:
        localValue += str(feature[letter])
    localValue = int(localValue)

    realValue = Terms["result"].value

    print("Meu Resultado =", localValue)
    print("Resultado Esperado =", realValue)
    realDist = abs(localValue - realValue)
    print("Distancia = ", realDist)
    return realDist


def makeSpecimen(quantity: int = 1):
    global Letters

    for i in range(quantity):
        SpecimenDict = {}
        random.seed()
        i = random.randint(0, len(PossibleValues))
        myValue = PossibleValues[i]
        del PossibleValues[i]

        for value, letter in zip(myValue, Letters):
            SpecimenDict[letter] = value

        Specimen(SpecimenDict, evalCapability)


init("send", 9567, "more", 1085, "money", 10652)
makeSpecimen()
getBestSpecimen()

