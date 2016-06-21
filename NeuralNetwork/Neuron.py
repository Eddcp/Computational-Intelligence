import typing

def binarySumActivation (inputs:tuple, weights:tuple) -> int :
    assert len(inputs) == len(weights), \
        "Input size doesn't match quantity of weights"

    s = 0
    for input, weight in zip(inputs, weights):
        s += input * weight

    return 1 if s > 0 else 0

class Neuron:

    def __init__(self, weights:list, activationFunction=binarySumActivation, learningRate=0.25,
                 maxWeight=1, minWeight=-1):
        self.weights = weights
        self.activationFunction = activationFunction
        self.learningRate = learningRate
        # self.maxWeight = maxWeight
        # self.minWeight = minWeight

    def __str__(self):
        weights = [format(x, '.2f') for x in self.weights]
        return str(weights)


    def train(self, expectation:int, inputs:tuple) -> int:
        assert len(inputs) == len(self.weights), \
            "Input size doesn't match quantity of weights"

        output = self.makeSinapse(inputs)
        error = expectation - output

        for i in range(len(self.weights)):
            self.weights[i] += self.learningRate * error * inputs[i]
            # self.weights[i] = max(self.weights[i], self.minWeight)
            # self.weights[i] = min(self.weights[i], self.maxWeight)
        return error


    def makeSinapse(self, inputs:tuple) -> int:
        assert len(inputs) == len(self.weights), \
            "Input size doesn't match quantity of weights"

        return self.activationFunction(inputs, self.weights)
