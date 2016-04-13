
import random
import collections
import logging



def cyclicCrossover(parent1:list, parent2:list, children:int=2) -> list:
    assert parent1 and parent2 and children in (1, 2)
    logging.debug("Parent1= %s", parent1)
    logging.debug("Parent2= %s", parent2)

    pos = random.randint(0, len(parent1)-1)

    p1, p2 = parent1, parent2

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

    child1, child2 = parent1[:], parent2[:]
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
    else:
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

    logging.debug("Swapped Range (%s, %s)", begin, end-1)

    p1, p2 = parent1, parent2
    child1, child2 = parent1[:], parent2[:]

    swap1, not_swap1 = set(), set()
    swap2, not_swap2 = set(), set()
    for i in range(len(parent1)):
        if i < begin or i > end-1:
            not_swap1.add(p1[i])
            not_swap2.add(p2[i])
        else:
            swap1.add(p1[i])
            swap2.add(p2[i])

    repeat1 = not_swap1 & swap2
    repeat2 = not_swap2 & swap1
    fixed1 = not_swap1 - repeat1
    fixed2 = not_swap2 - repeat2
    possibles1 = not_swap2 - fixed1
    possibles2 = not_swap1 - fixed2

    for i in range(len(p1)):
        if i >= begin and i < end:
            child1[i] = p2[i]
            child2[i] = p1[i]
        else:
            v1, v2 = p1[i], p2[i]
            if v1 in repeat1:
                if v2 in possibles1:
                    child1[i] = v2
                    possibles1.discard(v2)
                else:
                    child1[i] = possibles1.pop()
            if v2 in repeat2:
                if v1 in possibles2:
                    child2[i] = v1
                    possibles2.discard(v1)
                else:
                    child2[i] = possibles2.pop()

    logging.debug("Child=   %s", child1)
    logging.debug("Child=   %s", child2)
    logging.debug('')
    return (child1, child2)
# END pmx()



def main():
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s(): %(message)s')
    x = {"a":8, "b":4, "c":7, "d":3, "e":6, "f":2, "g":5, "h":1, "i":0}
    y = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8}
    dictCrossover(x, y, children=2)

if __name__ == "__main__":
    main()

def my_str(d:dict):
    return sorted(d.items())