import random

def getInputsFromTxt(file_name) -> tuple:
    file = open(file_name, mode='r')
    inputs = []
    for line in file:
        inputs.extend( [int(x) for x in line.split()] )

    return tuple(inputs)


def makeRandomWeights(quantity:int):
    weights = []
    for _ in range(quantity):
        mult = random.choice((1, -1))
        weights.append(random.random() * mult)

    return weights

def makeNullWeights(quantity:int):
    return [0] * quantity


def printWeigths(array, nrows=6, ncols=5):
    max_length = 0
    for x in array:
        max_length = max(max_length, len(str(x)))

    s = ' {:^' + str(max_length+3) + '} '
    s *= ncols
    s += '\n'
    s *= int(len(array) / ncols)

    return s.format(*array)


def printBinaryPixelMatrix(bins, nrows=6, ncols=5):
    s = ''
    for i, b in enumerate(bins):
        s += str(b)
        if i % ncols == ncols-1:
            s += '\n'
        else:
            s += ' '
    print(s)
