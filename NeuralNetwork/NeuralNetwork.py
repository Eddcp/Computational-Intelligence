import random
from Neuron import *
import typing as t
from Util import *

class NeuralNetwork:


    def __init__(self, numNeurons:int, numInputs:int, outputsMap:dict, randomWeights=False):
        assert len(tuple(outputsMap.keys())[0]) == numNeurons, \
            "Results from neurons don't have the same size as neurons quantity"

        makeWeights = makeRandomWeights if randomWeights else makeNullWeights

        self.neurons = []
        for _ in range(numNeurons):
            self.neurons.append(Neuron(makeWeights(numInputs)))

        self.outputsMap = outputsMap

    def __str__(self):
        s = ''
        for i in range(len(self.neurons)):
            s += "  Neuron {}:".format(i)
            if i % 10 == 0:
                s += "\n"
            s += str(self.neurons[i])
        s += '\n'
        return s

    # samples = varios padroes que serao analizados por todos os neuronios a cada
    #           epoca de treinamento
    # expectations = [[,],] expectativa de cada neuronio relacionado a um sample.
    def trainNetwork(self, samples, expectations, repeatFor:int=100, desirableError:int=0):
        assert len(samples) == len(expectations), \
            "Quantity of samples doesn't match quantity of expectations!"
        assert len(expectations[0]) == len(self.neurons), \
            "For each sample, it should have an expectation for each neuron!"

        totalError = desirableError + 1
        t = 0
        while (t < repeatFor) and (totalError > desirableError):
            totalError = 0
            t += 1
            print("     EPOCA {}".format(t))
            for sample, expectation in zip(samples, expectations):
                print()
                print("  SAMPLE: ", sample)
                print("  EXPECTATION: ", expectation)
                print()
                for i in range(len(self.neurons)):
                    print("neuronio ", i, "antes:", self.neurons[i])
                    error = abs(self.neurons[i].train(expectation[i], sample))
                    #neuronChanged = True if error else neuronChanged
                    totalError += error
                    print("neuronio ", i, "depois:", self.neurons[i])
                    print()
            # if not neuronChanged:
            #     break
            print()
        return t


    def analyze(self, pattern:tuple):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.makeSinapse(pattern))

        outputs = tuple(outputs)
        return self.outputsMap[outputs]
