import typing

class Neuron:

    def __init__(self, *weights, activationFunction=summationActivation, learningRate:int=1):
        self.weights = weights
        self.activationFunction = activationFunction
        self.learningRate = learningRate


    def train(self, expectation:int, *inputs:int):
        assert(len(inputs) == len(self.weights),
               "Input size doesn't match quantity of weights")

        output = self.makeSinapse(*inputs)
        error = abs(output - expectation)

        for i in range(len(self.weights)):
            self.weights[i] = self.learningRate * error * inputs[i]



    def train2(self, repeatFor:int, desirableError:int, learningRate:int, *samples,
              *expectations):
        assert(len(samples) == len(expectations),
               "Quantity of samples doesn't match quantity of expectations")
        assert(len(samples[0]) == len(self.weights),
               "Input size doesn't match quantity of weights")

        #TODO separar essa funcao: criar uma outra que treinaria todos os neuronios
        # varias vezes e com varios "samples"
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


    def makeSinapse(self, *inputs):
        assert(len(inputs) == len(self.weights),
               "Input size doesn't match quantity of weights")

        return self.activationFunction(inputs, self.weights)



def summationActivation (*inputs:int, *weights:int) -> int :
    assert(len(inputs) == len(weights),
           "Input size doesn't match quantity of weights")

    s = 0
    for input, weight in zip(inputs, weights):
        s += input * weights

    return s

