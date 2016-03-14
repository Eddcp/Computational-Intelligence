import random
import collections
import logging
logging.basicConfig(level=logging.DEBUG, format='%(funcName)s(): %(message)s')

def cyclicCrossover(parent1:dict, parent2:dict, children:int=1):
    assert parent1 and parent2 and children in range(1,3)
    logging.debug("Parent1= " + str(parent1))
    logging.debug("Parent2= " + str(parent2))

    # randomizing where to start the crossover
    for _ in range(len(parent1)):
        letter = random.choice(list(parent1.keys()))
        value1 = parent1[letter]
        value2 = parent2[letter]
        if value1 is not value2:
            break

    # seeing what can be changed in both parents in order to create a valid child.
    changed = collections.OrderedDict()
    for _ in range(len(parent1)):
        if value1 in changed:
            break
        changed[value1] = value2
        for letter in parent1.keys():
            if parent1[letter] == value2:
                value1 = value2
                value2 = parent2[letter]
                break
    logging.debug("{} letters changed. {}".format(len(changed), changed))

    # creating child
    childs = []
    parent = parent1
    for _ in range(children):
        child = {}
        for letter in parent:
            value = parent[letter]
            if value in changed:
                child[letter] = changed[value]
            else:
                child[letter] = value
        logging.debug("Child= " + str(child))
        childs.append(child)
        parent = parent2
    return childs



x = {"a":8, "b":4, "c":7, "d":3, "e":6, "f":2, "g":5, "h":1, "i":0}
y = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8}
cyclicCrossover(x, y, children=2)


