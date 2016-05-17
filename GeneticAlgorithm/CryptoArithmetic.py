import itertools
import random
import collections
import logging

from collections import Counter
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
    #Specimen.max_fitness = len(Letters)
    #Specimen.max_fitness = len(Result) * (BASE-1)



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

    dist_weight = 0.2
    hits_weight = 0.8

    hits_weight = LettersHitRate(alphabet) * hits_weight

    revision = 0
    # if len(Result) > max(*terms_length):
    #     most_significant = Result[0]
    #     if alphabet[most_significant] in (0, 1):
    #         revision = 0.25 * Specimen.max_fitness


    #if revision > 0.7:
    #    logging.debug(CA_str_values(alphabet))

    dist = evalResultsDist(alphabet) * dist_weight
    hits = Specimen.max_fitness * hits_weight
    eval = dist + hits
    #eval = min(Specimen.max_fitness, eval + revision)

    return eval


def LettersHitRate(alphabet:dict) -> float:
    #TODO inverter a ordem em que as letras dos termos e do resultado aparecem
    #TODO o problema esta no fato que o plus_one nao esta sendo calculado direito
    #TODO uma vez que as somas estao acontecendo do bit mais significativo pro menos
    global Result
    global Terms


# 'send' -> '_send'
    terms = []
    for term in Terms:
        #term = term[::-1]
        if len(Result) > len(term):
            most_significant = '_' * (len(Result) - len(term))
            term = most_significant + term
        terms.append(term)

    letters_hits = 0
    plus_one = 0
    for i in range(len(Result)-1, -1, -1):
        result_letter = Result[i]
        terms_letters = [term[i] for term in terms if term[i] is not '_']
        letters_values = [alphabet[letter] for letter in terms_letters]
        letters_value = sum(letters_values) + plus_one
        plus_one = 1 if letters_value >= BASE else 0
        if letters_value%BASE == alphabet[result_letter]:
            letters_hits += 1
    letters_hits_rate = (letters_hits / len(Result))
    return letters_hits_rate


def correct_letters(alphabet:dict):
    global Result
    global Terms
    global Letters
    global terms_length

# 'send' -> '_send'
    terms = []
    for term in Terms:
        #term = term[::-1]
        if len(Result) > len(term):
            most_significant = '_' * (len(Result) - len(term))
            term = most_significant + term
        terms.append(term)

    plus_one = False
    correct_letters = Counter()
    wrong_letters = set()
    debuff = 0
    previous_hit = False
    first_iteration = True
    for i in range(len(Result)-1, -1, -1):
        result_letter = Result[i]
        terms_letters = [term[i] for term in terms if term[i] is not '_']
        letters_values = [alphabet[letter] for letter in terms_letters]
        letters_sum = sum(letters_values)
        letters_sum_plus = letters_sum + 1
        current_letters = frozenset(terms_letters + list(result_letter))

        if letters_sum%BASE == alphabet[result_letter]:
            if not plus_one or not previous_hit:
                for letter in current_letters:
                    correct_letters[letter] += 1
                previous_hit = True
            else:
                for letter in current_letters:
                    wrong_letters.add(letter)
                previous_hit = False
            plus_one = True if letters_sum >= BASE else False

        elif not first_iteration and letters_sum_plus%BASE == alphabet[result_letter]:
            if plus_one or not previous_hit:
                for letter in current_letters:
                    correct_letters[letter] += 1
                previous_hit = True
            else:
                for letter in current_letters:
                    wrong_letters.add(letter)
                previous_hit = False
            plus_one = True if letters_sum_plus >= BASE else False
        else:
            for letter in current_letters:
                wrong_letters.add(letter)
            previous_hit = False
        first_iteration = False

    if len(Result) > max(*terms_length):
        most_significant = Result[0]
        if most_significant in correct_letters and alphabet[most_significant] not in (0, 1):
            debuff += max(1, correct_letters[most_significant])

    for letter in wrong_letters:
        debuff += correct_letters[letter]
    letters_hits = max(0, len(correct_letters) - debuff)
    letters_hits_rate = letters_hits / len(Letters)
    return letters_hits


def each_letter_dist(alphabet:dict):
    global Result
    global Terms

# 'send' -> '_send'
    terms = []
    for term in Terms:
        #term = term[::-1]
        if len(Result) > len(term):
            most_significant = '_' * (len(Result) - len(term))
            term = most_significant + term
        terms.append(term)

    letters_dist = 0
    plus_one = 0
    for i in range(len(Result)-1, -1, -1):
        result_letter = Result[i]
        terms_letters = [term[i] for term in terms if term[i] is not '_']
        letters_values = [alphabet[letter] for letter in terms_letters]
        letters_sum = sum(letters_values) + plus_one
        plus_one = 1 if letters_sum >= BASE else 0
        letters_sum = letters_sum % BASE
        letters_dist += abs(alphabet[result_letter] - letters_sum)

    return Specimen.max_fitness - letters_dist