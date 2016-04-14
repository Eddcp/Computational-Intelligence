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
terms_length = []
Result = None



def getExpression(*terms:str, result:str=None):
    global Letters
    global Terms
    global max_word_size
    global Result
    global terms_length

    assert(result)

    Result = result

    Letters = ''
    words = list(result) + list(terms)
    for word in words:
        for letter in word:
            if letter in Letters:
                continue
            Letters += letter
    Terms = terms
    terms_length = [len(x) for x in Terms]


    max_word_size = max(*terms_length, len(result))
    MAX_VALUE = 1 * BASE**(max_word_size)
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

    Specimen.setFitnessEvalFunction(betterEval)
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


def CA_str_values(alphabet:dict):
    global Result
    global Terms

    terms_value = [getWordValue(alphabet, x) for x in Terms]
    result = getWordValue(alphabet, Result)

    words = '  '
    for v, t in zip(terms_value, Terms):
        words += str(t) + ' = ' + str(v) + '    '
    words += Result + ' = ' + str(result)
    #logging.debug(words)

    sum_terms = sum(terms_value)
    sum_terms_str = ''
    for term in Terms:
        sum_terms_str += ' + '
        sum_terms_str += term
    summation = sum_terms_str + ' = ' + str(sum_terms)
    #logging.debug(summation)

    dist_string = '(' + sum_terms_str + ' )' + ' - ' + Result + ' = ' + str(abs(sum_terms - result))
    #logging.debug(dist_string)
    return words + '\n' + summation + '\n' + dist_string + '\n'


def betterEval(alphabet:dict) -> int:
    global Result
    global Terms
    global terms_length
    global Letters
    global max_word_size
    global BASE

    debuff = 0
    buff = 0

    if len(Result) > max(*terms_length):
        most_significant = Result[0]
        if alphabet[most_significant] in (0, 1):
            buff += 0.5

    terms = []
    for term in Terms:
        if len(Result) > len(term):
            left = ' ' * (len(Result) - len(term))
            term = left + term
        terms.append(term)

    letters_hits = 0
    for i, result_letter in enumerate(Result):
        terms_letters = [term[i] for term in terms if term[i] is not ' ']
        letters_value = [alphabet[letter] for letter in terms_letters]
        if sum(letters_value)%BASE == alphabet[result_letter]:
            letters_hits += 1
    buff += (letters_hits / len(Result))


    revision = abs(buff - debuff)

    return int(evalResultsDist(alphabet) * revision)