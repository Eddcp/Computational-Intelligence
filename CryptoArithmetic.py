import itertools
import random
import collections
import logging

from Specimen import *

BASE = 10
NUMBERS = range(BASE)

Letters = ""
MAX_VALUE = 0
max_word_size = 0
Terms = []
Result = None


def getExpression(result, *terms):
    global Letters
    global Terms
    global max_word_size
    global Result

    print(result)
    Result = result

    Letters = ''
    words = list(result) + list(terms)
    for word in words:
        for letter in word:
            if letter in Letters:
                continue
            Letters += letter
    Terms = terms

    max_word_size = len(result)
    MAX_VALUE = 0
    for i in range(max_word_size):
        MAX_VALUE += (BASE-1) * BASE**i
    Specimen.max_fitness = MAX_VALUE




# returns how far the specimen's result (mapped) is from the result evaluated through the expression
def evalResultsDist(alphabet: dict) -> int:
    global Terms
    global Result

    terms_value = (getWordValue(alphabet, x) for x in Terms)
    result = getWordValue(alphabet, Result)

    dist = abs(sum(terms_value) - result)

    return Specimen.max_fitness - dist



def makeSpecimen(quantity: int = 1) -> list:
    global Letters

    Specimen.setFitnessEvalFunction(evalResultsDist)
    population = []
    for i in range(quantity):
        specimenAlphabet = {}
        myValue = getPossibleValue()

        for value, letter in zip(myValue, Letters):
            specimenAlphabet[letter] = value

        population.append(Specimen(specimenAlphabet))

    return population

def getWordValue(alphabet: dict, word: str) -> int:
    value = ""
    for letter in word:
        value += str(alphabet[letter])
    return int(value)


def CA_str(self):
    s = "Chromosome={}  Fitness={}".format(sorted(self.chromosome.items()), self.fitness)
    return s
Specimen.__str__ = CA_str


def getPossibleValue():
    global NUMBERS

    numbers = list(NUMBERS)
    return random.sample(numbers, len(numbers))
