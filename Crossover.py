#TODO arrumar o crossover
# meu crossover ta com problema. Ele nao esta agindo da maneiro correta quando se quer mais de 1 filho.
# Ele nao esta verificando se a troca eh tambem valida no parent2; assim, ha grande possibilidade de
# se criar um filho nao valido(com valores repetidos para letras diferentes)

import random
import collections
import logging

def cyclicCrossover(parent1:dict, parent2:dict, children:int=1) -> list:
    assert parent1 and parent2 and children in (1, 2)
    logging.debug("Parent1= " + str(parent1))
    logging.debug("Parent2= " + str(parent2))

    # randomizing where to start the crossover
    # trying to get a position that can be changed
    for _ in range(len(parent1)):
        letter = random.choice(list(parent1.keys()))
        value1 = parent1[letter]
        value2 = parent2[letter]
        if value1 is not value2:
            # already got a position that can be changed
            break

    # seeing what can be changed in both parents in order to create a valid child.
    # making a "cyclic permutation"
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
        logging.debug("Child= {}\n".format(child))
        childs.append(child)
        parent = parent2

    return childs


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s(): %(message)s')
    x = {"a":8, "b":4, "c":7, "d":3, "e":6, "f":2, "g":5, "h":1, "i":0}
    y = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8}
    cyclicCrossover(x, y, children=2)

if __name__ == "__main__":
    main()

