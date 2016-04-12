#TODO arrumar o crossover
# meu crossover ta com problema. Ele nao esta agindo da maneiro correta quando se quer mais de 1 filho.
# Ele nao esta verificando se a troca eh tambem valida no parent2; assim, ha grande possibilidade de
# se criar um filho nao valido(com valores repetidos para letras diferentes)

import random
import collections
import logging

import CryptoArithmetic

def cyclicCrossover(parent1:list, parent2:list, children:int=2) -> list:
    assert parent1 and parent2 and children in (1, 2)
    logging.debug("Parent1= %s", parent1)
    logging.debug("Parent2= %s", parent2)

    pos = random.randint(0, len(parent1)-1)

    p1 = parent1
    p2 = parent2

    changed = collections.OrderedDict()
    before = p1[pos]
    after = p2[pos]
    hasDuplicates = True
    while hasDuplicates:
        changes = list(changed.items())
        if changes and changes[0][0] == changes[-1][1]:
            # chegou-se em um ciclo de alteracoes
            hasDuplicates = False
            break

        if after in changed:
            changed[before] = changes[0][0]
        else:
            changed[before] = after

        # ja faz as alteracoes nos vetores
        f1 = p1[:]
        f2 = p2[:]
        for i in range(len(p1)):
            if f1[i] == before:
                f1[i] = after
            if f2[i] == before:
                f2[i] = after

        for i in range(len(p1)):
            if i == pos:
                continue

            if f1[i] == after:
                before = after
                after = p2[i]
                pos = i
                hasDuplicates = True
                break
            elif f2[i] == after:
                before = after
                after = p1[i]
                pos = i
                hasDuplicates = True
                break
            aux = before
            before = after
            after = aux

    logging.debug("%s letters changed. %s", len(changed), changed)

    child1 = parent1[:]
    child2 = parent2[:]
    for i in range(len(parent1)):
        v1 = child1[i]
        v2 = child2[i]
        if v1 in changed:
            child1[i] = changed[v1]
        if v2 in changed:
            child2[i] = changed[v2]

    if children == 2:
        logging.debug("Child=   %s", child1)
        logging.debug("Child=   %s", child2)
        childs = (child1, child2)
    elif children == 1:
        childs = (child1)
        logging.debug("Child=   %s", child1)
    logging.debug('')

    return childs


def dictCrossover(parent1:dict, parent2:dict, children:int=2):
    p1_items = sorted(parent1.items())
    p1 = [v for (_, v) in p1_items]

    p2_items = sorted(parent2.items())
    p2 = [v for (_, v) in p2_items]

    keys = [k for (k, _) in p1_items]

    children = PMX(p1, p2)
    children_dicts = [dict() for _ in range(len(children))]

    for c in range(len(children)):
        for i, k in enumerate(keys):
            children_dicts[c][k] = children[c][i]

    return children_dicts



def PMX(parent1:list, parent2:list, children:int=2):

    logging.debug("Parent1= %s", parent1)
    logging.debug("Parent2= %s", parent2)

    begin = random.randint(0, len(parent1)-1)
    end = random.randint(begin+1, len(parent2))

    end = 1 if end is 0 else end

    logging.debug("Troca feita no seguinte intervalo (%s, %s)", begin, end-1)

    p1 = parent1[:]
    p2 = parent2[:]

    swap1 = set()
    rest1 = set()
    swap2 = set()
    rest2 = set()
    for i in range(len(parent1)):
        if i < begin or i > end:
            rest1.add(p1[i])
            rest2.add(p2[i])
        else:
            swap1.add(p1[i])
            swap2.add(p2[i])

    dup1 = rest1 & swap2
    dup2 = rest2 & swap1
    left1 = rest1 - dup1
    left2 = rest2 - dup2
    possibles1 = (dup2 | rest2) - left1
    possibles2 = (dup1 | rest1) - left2

    for i in range(len(p1)):
        if i >= begin and i < end:
            aux = p1[i]
            p1[i] = p2[i]
            p2[i] = aux
        elif p1[i] in dup1:
            p1[i] = possibles1.pop()
        elif p2[i] in dup2:
            p2[i] = possibles2.pop()

    logging.debug("Child=   %s", p1)
    logging.debug("Child=   %s", p2)
    logging.debug('')

    return (p1, p2)




def main():
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s(): %(message)s')
    x = {"a":8, "b":4, "c":7, "d":3, "e":6, "f":2, "g":5, "h":1, "i":0}
    y = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8}
    dictCrossover(x, y, children=2)

if __name__ == "__main__":
    main()

def my_str(d:dict):
    return sorted(d.items())


