import random
from Neuron import *
import typing as t

class NeuralNetwork:



    def __init__(self, numNeurons:int, numInputs:int, ):
        self.neurons = []
        for _ in range(numNeurons):
            self.neurons.append(Neuron(*_makeRandomWeights(numInputs)))


    def trainNetwork(self, samples:t.Sequence(t.Sequence), expectations:t.Sequence(t.Sequence),
                     repeatFor:int=1, desirableError:int=0):
        assert(len(samples) == len(expectations),
               "Quantity of samples doesn't match quantity of expectations")

        totalError = desirableError + 1
        t = 0
        while (t < repeatFor) and (totalError > desirableError):
            totalError = 0
            for i in range(len(self.weights)):
                output = self.makeSinapse(samples[i])
                error = abs(output - expectations[i])
                totalError += error
                self.weights[i] += learningRate * error * samples[i]
            t += 1



def _makeRandomWeights( quantity:int):
    weights = []
    for _ in range(quantity):
        weights.append(random.random())

    return tuple(weights)



