import itertools
import random

import collections

from Specimen import *
from Selection import *

NUMBERS = range(10)

Letters = ""
PossibleValues = []

Term = collections.namedtuple("Term", ["word", "value"])
Terms = {}


def init(populationSize:int=100, generations:int=50, fertilityRate:int=60, mutationRate:int=5):
    pass


def getExpression(first, firstValue, second, secondValue, result, resultValue):
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
    print("Number of permutations = ", len(PossibleValues))


# returns distance between the given real result and the "local" specimen's result (mapped)
def evalResultsDist(chromosome: dict) -> int:
    global Terms

    localValue = getWordValue(chromosome, Terms["result"].word)
    realValue = Terms["result"].value

    # print("Meu Resultado =", localValue)
    # print("Resultado Esperado =", realValue)
    dist = abs(localValue - realValue)
    # print("Distancia = ", dist)
    return dist


# returns how far the specimen's result (mapped) is from the result evaluated through the expression
def evalOperationDist(chromosome: dict) -> int:
    global Terms

    send = getWordValue(chromosome, "send")
    more = getWordValue(chromosome, "more")
    money = getWordValue(chromosome, "money")

    return abs(send+more - money)


def evalFitness(chromosome: dict) -> int:
    return evalOperationDist(chromosome)


def makeSpecimen(quantity: int = 1):
    global Letters

    for i in range(quantity):
        specimenAlphabet = {}
        random.seed()
        i = random.randint(0, len(PossibleValues))
        myValue = PossibleValues[i]
        del PossibleValues[i]

        for value, letter in zip(myValue, Letters):
            specimenAlphabet[letter] = value

        Specimen(specimenAlphabet, evalFitness)


def getWordValue(alphabet: dict, word: str) -> int:
    value = ""
    for letter in word:
        value += str(alphabet[letter])
    return int(value)

getExpression("send", 9567, "more", 1085, "money", 10652)
makeSpecimen(100)



best = Specimen.getBestSpecimen()
print("\nBest Specimen:\n", best, sep="")
send = getWordValue(best.chromosome, "send")
more = getWordValue(best.chromosome, "more")
money = getWordValue(best.chromosome, "money")
print("SEND = ", send)
print("MORE = ", more)
print("MONEY = ", money)
print("SEND + MORE = MONEY ?? ", send + more)
print("Real Capability = ", abs(send + more - 10652))

for x in Roulette(Specimen.Population):
    print(x)


# TODO Seleção(Torneio, Roleta); Crossover; Mutação; Gerações