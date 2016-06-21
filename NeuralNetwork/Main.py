from Neuron import *
from NeuralNetwork import *
from Util import *
from collections import defaultdict

number0 = getInputsFromTxt("Inputs/number0.txt")
number1 = getInputsFromTxt("Inputs/number1.txt")
number2 = getInputsFromTxt("Inputs/number2.txt")
number3 = getInputsFromTxt("Inputs/number3.txt")
number4 = getInputsFromTxt("Inputs/number4.txt")
number5 = getInputsFromTxt("Inputs/number5.txt")

number1_dist = getInputsFromTxt("Inputs/Distorted1/input11.txt")


def exercise1():

    outputsMap = {(0,): 0, (1,): 1}

    perceptron = NeuralNetwork(1, len(number0), outputsMap)

    samples = (number0, number1)
    expectations = ( (0,) , (1,) )

    epochs = perceptron.trainNetwork(samples, expectations)
    print("Treinamento demorou {} epocas".format(epochs))
    print(perceptron)

    print("Analisando o numero 0:")
    print(perceptron.analyze(number0))

    print("Analisando o numero 1:")
    print(perceptron.analyze(number1))

    print("Analisando o numero 2:")
    print(perceptron.analyze(number2))

    print("Analisando o numero 3:")
    print(perceptron.analyze(number3))

    print("Analisando o numero 4:")
    print(perceptron.analyze(number4))

    print("Analisando o numero 1 distorcido:")
    print(perceptron.analyze(number1_dist))

    print()
    print(printWeigths(perceptron.neurons[0].weights))

    printBinaryPixelMatrix(number1)


def exercise2():
    outputsMap = defaultdict(lambda:None)
    outputsMap[(1,0)] = 0
    outputsMap[(0,1)] = 1

    print(outputsMap[(1,1)])

    perceptron = NeuralNetwork(2, len(number0), outputsMap)

    samples = (number0, number1)
    expectations = ( (1,0) , (0,1) )

    epochs = perceptron.trainNetwork(samples, expectations)
    print("Treinamento demorou {} epocas".format(epochs))

    for x in perceptron.neurons:
        print(x)

    print("Analisando o numero 0:")
    print(perceptron.analyze(number0))

    print("Analisando o numero 1:")
    print(perceptron.analyze(number1))

    print("Analisando o numero 2:")
    print(perceptron.analyze(number2))

    print("Analisando o numero 3:")
    print(perceptron.analyze(number3))

    print("Analisando o numero 4:")
    print(perceptron.analyze(number4))

    print("Analisando o numero 5:")
    print(perceptron.analyze(number5))


def exercise3():
    outputsMap = defaultdict(lambda:None)
    outputsMap[(1,0,0,0,0,0)] = 0
    outputsMap[(0,1,0,0,0,0)] = 1
    outputsMap[(0,0,1,0,0,0)] = 2
    outputsMap[(0,0,0,1,0,0)] = 3
    outputsMap[(0,0,0,0,1,0)] = 4
    outputsMap[(0,0,0,0,0,1)] = 5

    perceptron = NeuralNetwork(6, len(number0), outputsMap, randomWeights=True)

    samples = (number0, number1, number2, number3, number4, number5)
    expectations = ( (1,0,0,0,0,0), (0,1,0,0,0,0), (0,0,1,0,0,0), (0,0,0,1,0,0),
                     (0,0,0,0,1,0), (0,0,0,0,0,1) )

    epochs = perceptron.trainNetwork(samples, expectations)
    print("Treinamento demorou {} epocas".format(epochs))

    for x in perceptron.neurons:
        print(x)

    print()
    print("Analisando o numero 0:")
    print(perceptron.analyze(number0))

    print("Analisando o numero 1:")
    print(perceptron.analyze(number1))

    print("Analisando o numero 2:")
    print(perceptron.analyze(number2))

    print("Analisando o numero 3:")
    print(perceptron.analyze(number3))

    print("Analisando o numero 4:")
    print(perceptron.analyze(number4))

    print("Analisando o numero 5:")
    print(perceptron.analyze(number5))

    print("Analisando o numero 1 distorcido:")
    print(perceptron.analyze(number1_dist))


if __name__ == "__main__":
    number0 = getInputsFromTxt("Inputs/number0.txt")
    number1 = getInputsFromTxt("Inputs/number1.txt")

    neuron = Neuron(makeNullWeights(len(number0)))
    print(neuron)
    neuron.train(1, number1)
    print(neuron)
    neuron.train(0, number0)
    print(neuron)

    print(neuron.makeSinapse(number0))
    print(neuron.makeSinapse(number1))


    exercise1()




