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
    print("Number of permutations = ", len(PossibleValues))


# returns distance between the given real result and the "local" specimen's result (mapped)
def evalResultsDist(feature: dict) -> int:
    global Terms

    localValue = getWordValue(feature, Terms["result"].word)
    realValue = Terms["result"].value

    # print("Meu Resultado =", localValue)
    # print("Resultado Esperado =", realValue)
    dist = abs(localValue - realValue)
    # print("Distancia = ", dist)
    return dist


# returns how far the specimen's result (mapped) is from the result evaluated through the expression
def evalOperationDist(feature: dict) -> int:
    global Terms

    send = getWordValue(feature, "send")
    more = getWordValue(feature, "more")
    money = getWordValue(feature, "money")

    return abs(send+more - money)


def evalCapability(feature: dict) -> int:
    opDist = evalOperationDist(feature)
    resDist = evalResultsDist(feature)

    return (opDist + resDist)/2


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

        Specimen(specimenAlphabet, evalOperationDist)


def getWordValue(alphabet: dict, word: str) -> int:
    value = ""
    for letter in word:
        value += str(alphabet[letter])
    return int(value)

init("send", 9567, "more", 1085, "money", 10652)
makeSpecimen(100)



best = Specimen.getBestSpecimen()
print("\nBest Specimen:\n", best, sep="")
send = getWordValue(best.feature, "send")
more = getWordValue(best.feature, "more")
money = getWordValue(best.feature, "money")
print("SEND = ", send)
print("MORE = ", more)
print("MONEY = ", money)
print("SEND + MORE = MONEY ?? ", send + more)
print("Real Capability = ", abs(send + more - 10652))
