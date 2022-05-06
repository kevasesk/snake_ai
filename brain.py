import numpy as np
import random, math


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


def sigmoidList(list):
    for i in range(len(list)):
        list[i] = sigmoid(list[i])
    return list


def networkInit(input, hidden1, output_count):
    input = 1 / np.array(input)
    w1 = np.random.rand(len(input), hidden1)
    z1 = sigmoidList(np.matmul(input, w1))
    w2 = np.random.rand(hidden1, output_count)
    output = sigmoidList(np.matmul(z1, w2))
    direction = np.argmax(output)
    return w1, w2, direction

def networkBuild(input, w1, w2):
    input = 1 / np.array(input)
    z1 = sigmoidList(np.matmul(input, w1))
    output = sigmoidList(np.matmul(z1, w2))
    direction = np.argmax(output)
    return direction


w1, w2, direction = networkInit([1, 2, 1], 2, 4)
