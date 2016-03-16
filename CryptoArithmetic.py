import itertools
import random
import collections
import logging

from Specimen import *

BASE = 10
NUMBERS = range(BASE)

Letters = ""
PossibleValues = []

Term = collections.namedtuple("Term", ["word", "value"])
Terms = {}


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
    logging.debug("Number of permutations = {}".format(len(PossibleValues)))


# returns distance between the given real result and the "local" specimen's result (mapped)
def evalResultsDist(alphabet: dict) -> int:
    global Terms

    localValue = getWordValue(alphabet, Terms["result"].word)
    realValue = Terms["result"].value

    # print("Meu Resultado =", localValue)
    # print("Resultado Esperado =", realValue)
    dist = abs(localValue - realValue)
    # print("Distancia = ", dist)
    return dist


# returns how far the specimen's result (mapped) is from the result evaluated through the expression
def evalOperationDist(alphabet: dict) -> int:
    global Terms
    global Letters
    global BASE

    term1 = getWordValue(alphabet, Terms["first"].word)
    term2 = getWordValue(alphabet, Terms["second"].word)
    result = getWordValue(alphabet, Terms["result"].word)

    max_value = 0
    for i in range(len(Letters)):
        max_value += (BASE-1) * BASE**i

    return max_value - abs(term1+term2 - result)


def evalFitness(alphabet: dict) -> int:
    return evalOperationDist(alphabet)


def makeSpecimen(quantity: int = 1) -> list:
    global Letters

    Specimen.setFitnessEvalFunction(evalFitness)
    population = []
    for i in range(quantity):
        specimenAlphabet = {}
        random.seed()
        i = random.randint(0, len(PossibleValues))
        myValue = PossibleValues[i]
        del PossibleValues[i]

        for value, letter in zip(myValue, Letters):
            specimenAlphabet[letter] = value

        population.append(Specimen(specimenAlphabet))

    return population

def getWordValue(alphabet: dict, word: str) -> int:
    value = ""
    for letter in word:
        value += str(alphabet[letter])
    return int(value)





# TODO Seleção(Torneio, Roleta); Crossover; Mutação; Gerações